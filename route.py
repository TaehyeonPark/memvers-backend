import fastapi
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from uvicorn import run
from typing import List, Dict, Any, Union, Optional

from sqlalchemy.orm import Session

from database import SessionLocal, engine, get_db
import crud, models, schema, crud_v2

app = fastapi.FastAPI()

@app.get("/")
async def root():
    return RedirectResponse(url="/docs")

@app.post("/api/v2/insert/{table}")
async def insert(table: str, data: Dict[str, Any], db: Session = fastapi.Depends(get_db)):
    if table not in models.TABLES:
        return {"detail": f"{table} is not in schema"}
    if data['nickname'] == None and table != None and data != None:
        return {"status": 400, "message": f"REQ => insert {table} | Bad Request", "data": None}
    return crud_v2.insert(db, table, data)

@app.post("/api/v2/update/{table}")
async def update(table: str, data: Dict[str, Any], db: Session = fastapi.Depends(get_db)):
    if table not in models.TABLES:
        return {"detail": f"{table} is not in schema"}
    if data['nickname'] == None and table != None and data != None:
        return {"status": 400, "message": f"REQ => update {table} | Bad Request", "data": None}
    return crud_v2.update(db, table, data)

@app.post("/api/v2/read/{table}")
async def read(table: str, data: Dict[str, Any], db: Session = fastapi.Depends(get_db)):
    if table not in models.TABLES:
        return {"detail": f"{table} is not in schema"}
    if data['nickname'] == None and table != None and data != None:
        return {"status": 400, "message": f"REQ => read {table} | Bad Request", "data": None}
    return crud_v2.read(db, table, data)

@app.get("/api/v2/help")
async def example_for_dummy_data(data: Optional[schema.HELP] = None, request: fastapi.Request = None):
    return Jinja2Templates(directory="templates").TemplateResponse("help.html", context={"request": request})


if __name__ == '__main__':
    run(host='0.0.0.0', port=8000, app=app)
    