import fastapi
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi import Depends

from uvicorn import run
from typing import List, Dict, Any, Union, Optional

from sqlalchemy.orm import Session
from redis import Redis

from json import loads

from database import SessionLocal, engine, get_db
import models, schema, crud_v2
import ldap

app = fastapi.FastAPI()

@app.get("/")
async def root():
    # return RedirectResponse(url="/docs")
    return {"status": 200, "message": "Welcome to NUGU API Server", "data": None}

@app.get("/api/v1/help")
async def example_for_dummy_data(data: Optional[schema.HELP] = None, request: Request = None):
    return Jinja2Templates(directory="templates").TemplateResponse("help.html", context={"request": request})

@app.get("/api/v2/help")
async def example_for_dummy_data(data: Optional[schema.HELP] = None, request: Request = None):
    return Jinja2Templates(directory="templates").TemplateResponse("help.html", context={"request": request})

@app.post("/api/v2/insert/{table}")
async def insert(table: str, data: Dict[str, Any], db: Session = Depends(get_db)):
    if table not in models.TABLES:
        return {"detail": f"{table} is not in schema"}
    if data['nickname'] == None and table != None and data != None:
        return {"status": 400, "message": f"REQ => Fail to insert {table} | Bad Request", "data": None}
    return crud_v2.insert(db, table, data)

@app.post("/api/v2/update/{table}")
async def update(table: str, data: Dict[str, Any], db: Session = Depends(get_db)):
    if table not in models.TABLES:
        return {"detail": f"{table} is not in schema"}
    if data['nickname'] == None and table != None and data != None:
        return {"status": 400, "message": f"REQ => Fail to update {table} | Bad Request", "data": None}
    return crud_v2.update(db, table, data)

# @app.post("/api/v2/read/{table}")
# async def read(table: str, data: schema.READ, db: Session = Depends(get_db)):
#     data, mode = data.data, data.mode
#     print(data, mode)
#     if table not in models.TABLES:
#         return {"detail": f"{table} is not in schema", "data": None}

#     _data = data.copy()
#     _keys = None
#     for i in models.KEYS:
#         _table = list(i.keys())[0]
#         if _table == table:
#             _keys = i[_table]
#             break
#     for _key in list(_data.keys()):
#         if _key not in _keys:
#             _data.pop(_key)
#     rtn = crud_v2.read(db, table, _data, mode=mode.upper())
    
#     return {"status": 200, "message": f"REQ => Success to read {table}", "data": rtn}

@app.post("/api/v2/read/{table}")
async def read(request: Request, db: Session = Depends(get_db)):
    if request.path_params['table'] not in models.TABLES:
        return {"detail": f"{request.path_params['table']} is not in schema", "data": None}
    
    table = request.path_params['table']
    formData = await request.form()
    data = loads(formData['data'])
    mode = formData['mode']
    _data = data.copy()
    _keys = None

    for i in models.KEYS:
        _table = list(i.keys())[0]
        if _table == table:
            _keys = i[_table]
            break
    for _key in list(_data.keys()):
        if _key not in _keys:
            _data.pop(_key)
            
    rtn = crud_v2.read(db, table, _data, mode=mode.upper())
    
    return {"status": 200, "message": f"REQ => Success to read {table}", "data": rtn}

@app.get("/client")
async def client(request: Request):
    return Jinja2Templates(directory="client").TemplateResponse("client_v2.html", context={"request": request})

if __name__ == '__main__':
    run(host='0.0.0.0', port=8000, app=app)