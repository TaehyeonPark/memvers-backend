from fastapi import FastAPI, Depends, HTTPException, status, Request, Response, Form, Cookie, Header
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

app = FastAPI()

redi = Redi(host="localhost", port=6378, db=0)

@app.get("/", include_in_schema=False)
@app.get("/index", include_in_schema=False)
async def root(request: Request):
    return {"status": 200, "msg": "Welcome to memvers API Server. If you need help, goto /help", "data": None}

@app.get("/logout", include_in_schema=False)
async def logout(request: Request):
    redi.delete(request.client.host)
    return RedirectResponse(url="/login", status_code=302)

@app.post("/login")
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

@app.get("/search")
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

@app.post("/add")
async def add(request: Request, db: Session = Depends(get_db)): 
    jsondata = await request.json()

    if not redi.get(request.cookies.get("uuid")) == jsondata['nickname']:
        return JSONResponse(content={"status": "400", "msg": "Bad Request"})

    for key in models.get_keys_from_table(table=jsondata['table']):
        if key not in jsondata.keys():
            jsondata[key] = models.yield_default_value_type_by_key(table=jsondata['table'], key=key)
        jsondata[key] = models.type_casting_by_table(table=jsondata['table'], key=key, data=jsondata[key])
    print(jsondata)
    if crud.insert(db=db, table=jsondata['table'], data=jsondata):
        return JSONResponse(content={"status": "200", "msg": "success"})
    else:
        return JSONResponse(content={"status": "400", "msg": "Bad Request"})

@app.post("/edit")
async def edit(request: Request, db: Session = Depends(get_db)):
    jsondata = await request.json()

    if not redi.get(request.cookies.get("uuid")) == jsondata['nickname']:
        return JSONResponse(content={"status": "400", "msg": "Bad Request"})

    oldcontents = jsondata['oldcontents']
    newcontents = jsondata['newcontents']
    del jsondata['oldcontents']
    del jsondata['newcontents']
    oldcontents['nickname'] = jsondata['nickname']
    newcontents['nickname'] = jsondata['nickname']
    
    print(oldcontents)
    print(newcontents)

    for key in models.get_keys_from_table(table=jsondata['table']):
        if key not in newcontents.keys():
            newcontents[key] = models.yield_default_value_type_by_key(table=jsondata['table'], key=key)
        newcontents[key] = models.type_casting_by_table(table=jsondata['table'], key=key, data=newcontents[key])
        if key not in oldcontents.keys():
            oldcontents[key] = models.yield_default_value_type_by_key(table=jsondata['table'], key=key)
        oldcontents[key] = models.type_casting_by_table(table=jsondata['table'], key=key, data=oldcontents[key])
    
    print(oldcontents)
    print(newcontents)
    
    if crud.edit(db=db, table=jsondata['table'], olddata=oldcontents, newdata=newcontents):
        print("success")
        return JSONResponse(content={"status": "200", "msg": "success"})
    else:
        print("failed")
        return JSONResponse(content={"status": "400", "msg": "Bad Request"})

@app.post("/delete")
async def delete(request: Request, db: Session = Depends(get_db)):
    jsondata = await request.json()

    if not redi.get(request.cookies.get("uuid")) == jsondata['nickname']:
        return JSONResponse(content={"status": "400", "msg": "Bad Request"})

    for key in models.get_keys_from_table(table=jsondata['table']):
        if key not in jsondata.keys():
            jsondata[key] = models.yield_default_value_type_by_key(table=jsondata['table'], key=key)
        jsondata[key] = models.type_casting_by_table(table=jsondata['table'], key=key, data=jsondata[key])
    print(jsondata)
    if crud.delete(db=db, table=jsondata['table'], data=jsondata):
        print("success")
        return JSONResponse(content={"status": "200", "msg": "success"})
    else:
        print("failed")
        return JSONResponse(content={"status": "400", "msg": "Bad Request"})

@app.middleware("http")
async def session_managing_middleware(request: Request, call_next):
    response = await call_next(request)
    if request.url.path == "/login":
        return response
    if not IsUUIDValid(request, redi) and request.url.path != "/login":
        return RedirectResponse(url="/login", status_code=302)
    return response

@app.exception_handler(404)
async def not_found(request: Request, exc: Exception):
    return JSONResponse(content={"status": "404", "msg": "Not Found"}, status_code=404)

@app.exception_handler(401)
async def unauthorized_handler(request: Request, exc: Exception):
    return RedirectResponse(url="/login", status_code=302)

@app.exception_handler(500)
async def internal_server_error_handler(request: Request, exc: Exception):
    return JSONResponse(content={"status": "500", "msg": "Internal Server Error"}, status_code=500)

@app.exception_handler(422)
async def unprocessable_entity_handler(request: Request, exc: Exception):
    return JSONResponse(content={"status": "422", "msg": "Unprocessable Entity. The request was well-formed but was unable to be followed due to semantic errors."}, status_code=422)
if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8000)