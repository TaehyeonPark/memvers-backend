import fastapi
from uvicorn import run
from typing import List, Dict, Any, Union

from sqlalchemy.orm import Session

from database import SessionLocal, engine, get_db
import crud, models, schema, crud_v2

app = fastapi.FastAPI()

@app.post("/api/v2/insert/{table}")
async def insert(table: str, data: Dict[str, Any], db: Session = fastapi.Depends(get_db)):
    if table not in models.TABLES:
        return {"detail": f"{table} is not in schema"}
    if data['nickname'] == None and table != None and data != None:
        return {"status": 400, "message": f"REQ => insert {table} | Bad Request"}
    return crud_v2.insert(db, table, data)

@app.post("/api/v2/update/{table}")
async def update(table: str, data: Dict[str, Any], db: Session = fastapi.Depends(get_db)):
    if table not in models.TABLES:
        return {"detail": f"{table} is not in schema"}
    if data['nickname'] == None and table != None and data != None:
        return {"status": 400, "message": f"REQ => update {table} | Bad Request"}
    return crud_v2.update(db, table, data)

@app.post("/api/v2/read/{table}")
async def read(table: str, data: Dict[str, Any], db: Session = fastapi.Depends(get_db)):
    if table not in models.TABLES:
        return {"detail": f"{table} is not in schema"}
    if data['nickname'] == None and table != None and data != None:
        return {"status": 400, "message": f"REQ => read {table} | Bad Request"}
    return crud_v2.read(db, table, data)



@app.get("/api/v1/nugu/create")
async def create_nugu(nugu: schema.INSERT = None, db: Session = fastapi.Depends(get_db)):
    print(nugu)
    return {"status": 200, "message": "server is running"}
    # return {"detail": f"{nugu.Nugu.nickname} already registered"} if crud.exist_nugu(db, key="nickname", value=nugu.Nugu.nickname) else crud.insert_nugu(db=db, nugu=nugu)

@app.post("/api/v1/nugu/create")
async def create_nugu(nugu: schema.INSERT = None, db: Session = fastapi.Depends(get_db)):
    return {"detail": f"{nugu.Nugu.nickname} already registered"} if crud.exist_nugu(db, key="nickname", value=nugu.Nugu.nickname) else crud.insert_nugu(db=db, nugu=nugu)

@app.get("/api/v1/nugu/read")
async def get_nugu(key: str = None, value: str = None, mode: str = "exact", db: Session = fastapi.Depends(get_db)):
    return crud.get_nugu(db, key=key, value=value, mode=mode)
    
@app.post("/api/v1/nugu/read")
async def get_nugu(key: str = None, value: str = None, mode: str = "exact", db: Session = fastapi.Depends(get_db)):
    return crud.get_nugu(db, key=key, value=value, mode=mode)

@app.get("/api/v1/nugu/update/{nickname}")
async def edit_nugu(nickname: str, nugu: schema.Nugu, db: Session = fastapi.Depends(get_db)):
    return {"detail": f"{nugu.nickname} already registered"} if crud.exist_nugu(db, key="nickname", value=nugu.nickname) else crud.update_nugu(db=db, nugu=nugu)

@app.post("/api/v1/nugu/update")
async def edit_nugu(nugu: schema.Nugu, db: Session = fastapi.Depends(get_db)):
    return {"detail": f"{nugu.nickname} already registered"} if crud.exist_nugu(db, key="nickname", value=nugu.nickname) else crud.update_nugu(db=db, nugu=nugu)

if __name__ == '__main__':
    run(host='0.0.0.0', port=8000, app=app)
    