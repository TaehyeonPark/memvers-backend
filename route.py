import fastapi
from uvicorn import run
from typing import List, Dict, Any, Union

from sqlalchemy.orm import Session

from database import SessionLocal, engine, get_db
import crud, models, schema

app = fastapi.FastAPI()

@app.post("/api/v2/{nickname}/{table}/create")
async def create(nickname: str, table: str, data: Dict[str, Any], db: Session = fastapi.Depends(get_db)):
    print(nickname, table, data)
    if nickname == data["nickname"]:
        return {"status": 200, "message": "Server is running"}
    return {"status": 400, "message": "Something went wrong"}
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
    