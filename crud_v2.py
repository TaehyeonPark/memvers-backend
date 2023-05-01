from sqlalchemy import text
from sqlalchemy.orm import Session
import pymysql

from typing import Dict

import models, schema
from util import Comp, Validate

PK = models.Nugu.nickname.__str__().split(".")[-1]
HANDLER = ["create", "read", "update"]

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

def _execute(db: Session, query: str = None):
    try:
        db.execute(query)
        db.commit()
        return True, {"status": 200, "message": f"REQ | Successfully executed"}
    except Exception as e:
        return False, e

def _achivement_duplicate_check(db: Session, data: Dict = None):
    try:
        cursor = db.execute(text(f"SELECT * FROM achivement WHERE nickname='{data['nickname']}' AND content='{data['content']}'"))  # True: exist, False: not exist => insert only if not exist(=False)
        if cursor.rowcount > 0:
            return True
        return False
    except Exception as e:
        return {"status": 500, "message": f"REQ | achivement | {e}"}

def insert(db: Session, table: str = None, data: Dict = None):
    try:
        if table == "achivement":
            if _achivement_duplicate_check(db=db, data=data):
                return {"status": 400, "message": f"REQ | {table} | Already exist"}
        rtn, msg = _execute(db=db, query=text(f"INSERT INTO {table} VALUES {tuple(data.values())}"))
        return msg if rtn else {"status": 500, "message": f"REQ | {table} | {msg}"}
    except Exception as e:
        return {"status": 500, "message": f"REQ | {table} | {e}"}

def update(db: Session, nickname=None, table: str = None, data: Dict = None):
    try:
        rtn, msg = _execute(db=db, query=text(f"UPDATE {table} SET {', '.join([f'{key}={value}' for key, value in data.items()])} WHERE {PK}='{nickname}'"))
        return msg if rtn else {"status": 500, "message": f"REQ | {table} | {msg}"}
    except Exception as e:
        return {"status": 500, "message": f"REQ | {table} | {e}"}