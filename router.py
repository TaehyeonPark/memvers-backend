from fastapi import FastAPI, HTTPException, status, Request, Response, APIRouter
from fastapi import Depends, Form, Cookie, Header
from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi_sessions.backends.implementations import InMemoryBackend

from sqlalchemy.orm import Session

from uvicorn import run

import uuid
from json import loads, dumps
from typing import Optional, List, Dict, Any

import models, schema, crud
import ldap
from inmemorydb import Redi
from database import SessionLocal, engine, get_db
from util import *
from session import *
from error_template import error_template

router = APIRouter()
redi = Redi(host="localhost", port=6378, db=0)

@router.get("/", include_in_schema=False)
@router.get("/index", include_in_schema=False)
async def root(request: Request):
    return {"status": 200, "msg": "Welcome to memvers API Server. If you need help, goto /help", "data": None}

@router.get("/logout", include_in_schema=False)
async def logout(request: Request):
    redi.delete(request.client.host)
    return RedirectResponse(url="/login", status_code=302)

@router.post("/login")
async def login(request: Request):
    __formData = await request.form()
    if ldap.bind(__formData.get("id"), __formData.get("pw")):
        __uuid = uuid.uuid4().hex
        redi.set(request.client.host, __uuid, ex=60*60)
        redi.set(__uuid, __formData.get("id"), ex=60*60)
        _response = JSONResponse(content={"result": "success" , "status": 200, "msg": "Login Success"})
        _response.set_cookie(key="uuid", value=__uuid)
        return _response
    else:
        return JSONResponse(content={"result": "failed"})

@router.get("/search")
async def memvers(request: Request, db: Session = Depends(get_db)):
    """
    # TODO: Implement authentication
    """
    params = request.query_params
    rtn = crud.search(db=db, table=params.get("table"), key=params.get("column"), data=params.get("content"), mode=params.get("mode"))
    if type(rtn) == list:
        return JSONResponse(content={"status": "200", "msg": "success", "data": rtn})
    else:
        return JSONResponse(content={"status": "400", "msg": "Bad Request"})

@router.post("/add")
async def add(request: Request, db: Session = Depends(get_db)): 
    jsonData = await request.json()

    if not redi.get(request.cookies.get("uuid")) == jsonData['nickname']:
        return JSONResponse(content={"status": "400", "msg": "Bad Request"})

    for key in models.get_keys_from_table(table=jsonData['table']):
        if key not in jsonData.keys():
            jsonData[key] = models.yield_default_value_type_by_key(table=jsonData['table'], key=key)
        jsonData[key] = models.type_casting_by_table(table=jsonData['table'], key=key, data=jsonData[key])
    print(jsonData)
    if crud.insert(db=db, table=jsonData['table'], data=jsonData):
        return JSONResponse(content={"status": "200", "msg": "success"})
    else:
        return JSONResponse(content={"status": "400", "msg": "Bad Request"})

@router.post("/edit")
async def edit(request: Request, db: Session = Depends(get_db)):
    jsonData = await request.json()

    if not redi.get(request.cookies.get("uuid")) == jsonData['nickname']:
        return JSONResponse(content={"status": "400", "msg": "Bad Request"})

    if jsonData['table'] == 'ldap':
        if ldap.resetPassword(un=jsonData['nickname'], npass=jsonData["pw"], adminpw=jsonData["adminpw"]):
            return JSONResponse(content={"status": "200", "msg": "success"})
        return JSONResponse(content={"status": "400", "msg": "Bad Request"})


    oldcontents = jsonData['oldcontents']
    newcontents = jsonData['newcontents']
    del jsonData['oldcontents']
    del jsonData['newcontents']
    oldcontents['nickname'] = jsonData['nickname']
    newcontents['nickname'] = jsonData['nickname']
    
    print(oldcontents)
    print(newcontents)

    for key in models.get_keys_from_table(table=jsonData['table']):
        if key not in newcontents.keys():
            newcontents[key] = models.yield_default_value_type_by_key(table=jsonData['table'], key=key)
        newcontents[key] = models.type_casting_by_table(table=jsonData['table'], key=key, data=newcontents[key])
        if key not in oldcontents.keys():
            oldcontents[key] = models.yield_default_value_type_by_key(table=jsonData['table'], key=key)
        oldcontents[key] = models.type_casting_by_table(table=jsonData['table'], key=key, data=oldcontents[key])
    
    print(oldcontents)
    print(newcontents)
    
    if crud.edit(db=db, table=jsonData['table'], olddata=oldcontents, newdata=newcontents):
        print("success")
        return JSONResponse(content={"status": "200", "msg": "success"})
    else:
        print("failed")
        return JSONResponse(content={"status": "400", "msg": "Bad Request"})

@router.post("/delete")
async def delete(request: Request, db: Session = Depends(get_db)):
    jsonData = await request.json()

    if not redi.get(request.cookies.get("uuid")) == jsonData['nickname']:
        return JSONResponse(content={"status": "400", "msg": "Bad Request"})

    for key in models.get_keys_from_table(table=jsonData['table']):
        if key not in jsonData.keys():
            jsonData[key] = models.yield_default_value_type_by_key(table=jsonData['table'], key=key)
        jsonData[key] = models.type_casting_by_table(table=jsonData['table'], key=key, data=jsonData[key])
    print(jsonData)
    if crud.delete(db=db, table=jsonData['table'], data=jsonData):
        print("success")
        return JSONResponse(content={"status": "200", "msg": "success"})
    else:
        print("failed")
        return JSONResponse(content={"status": "400", "msg": "Bad Request"})
