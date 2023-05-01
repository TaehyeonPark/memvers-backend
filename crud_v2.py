from sqlalchemy import text
from sqlalchemy.orm import Session

from typing import Dict

import models, schema
from util import Comp, Validate

PK = models.Nugu.nickname.__str__().split(".")[-1]

comp = Comp()
val = Validate(PK=PK)

def _exist(db: Session, table: str = None, key: str = None, value: str = None):
    if table not in models.TABLES:
        return {"status": 404, "message": f"REQ {table} | Not Found"}
    if not key or not value:
        return {"status": 400, "message": f"REQ {table} | Bad Request"}
    try:
        db_any = (db.query(getattr(models, table)).filter(getattr(models, table).__dict__[key] == value).first().__dict__)
        if db_any:
            return True
    except Exception as e:
        pass
    return False
def insert(db: Session, nickname=None, table: str = None, data: Dict = None):
    if table not in models.TABLES:
        return {"status": 404, "message": f"REQ {table} | Not Found"}
    if not data:
        return {"status": 400, "message": f"REQ {table} | Bad Request"}
    if not nickname:
        return {"status": 400, "message": f"REQ {table} | Bad Request"}
    try:
        query = text(f"INSERT INTO {table} VALUES {tuple(data.values())}")
        db.execute(query)
        db.commit()
        return {"status": 200, "message": f"REQ {table} | Successfully inserted"}
    except Exception as e:
        return {"status": 500, "message": f"REQ {table} | {e}"}