import fastapi
from typing import List, Dict, Any, Union

from sqlalchemy.orm import Session

from database import SessionLocal, engine
import crud, models, schema

app = fastapi.FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/v1/nugu/create")
async def create_nugu(nugu: schema.Nugu = None, db: Session = fastapi.Depends(get_db)):
    return {"detail": f"{nugu.nickname} already registered"} if crud.exist_nugu(db, key="nickname", value=nugu.nickname) else crud.insert_nugu(db=db, nugu=nugu)

@app.post("/api/v1/nugu/create")
async def create_nugu(nugu: schema.Nugu = None, db: Session = fastapi.Depends(get_db)):
    return {"detail": f"{nugu.nickname} already registered"} if crud.exist_nugu(db, key="nickname", value=nugu.nickname) else crud.insert_nugu(db=db, nugu=nugu)

@app.get("/api/v1/nugu/read")
async def get_nugu(key: str = None, value: str = None, mode: str = "exact", db: Session = fastapi.Depends(get_db)):
    return crud.get_nugu(db, key=key, value=value, mode=mode)
    
@app.post("/api/v1/nugu/read")
async def get_nugu(key: str = None, value: str = None, mode: str = "exact", db: Session = fastapi.Depends(get_db)):
    return crud.get_nugu(db, key=key, value=value, mode=mode)

@app.get("/api/v1/nugu/update")
async def edit_nugu(nugu: schema.Nugu, db: Session = fastapi.Depends(get_db)):
    return {"detail": f"{nugu.nickname} already registered"} if crud.exist_nugu(db, key="nickname", value=nugu.nickname) else crud.update_nugu(db=db, nugu=nugu)

@app.post("/api/v1/nugu/update")
async def edit_nugu(nugu: schema.Nugu, db: Session = fastapi.Depends(get_db)):
    return {"detail": f"{nugu.nickname} already registered"} if crud.exist_nugu(db, key="nickname", value=nugu.nickname) else crud.update_nugu(db=db, nugu=nugu)
