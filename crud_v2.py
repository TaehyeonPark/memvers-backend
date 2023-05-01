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

def _execute(db: Session, query: str = None):
    try:
        cursor = db.execute(query)
        db.commit()
        if cursor.rowcount > 0:
            return True, {"status": 200, "message": f"REQ | Successfully executed"}
        return False, {"status": 400, "message": f"REQ | Failed to execute"}
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

def update(db: Session, table: str = None, data: Dict = None): # Needed: Different edition level by privilige.
    try:
        update_list = []
        for key, value in data.items():
            if key == PK:
                continue
            if value == None or value == '':
                continue
            update_list.append(f"{key}={value}")
        rtn, msg = _execute(db=db, query=text(f"UPDATE {table} SET {', '.join(update_list)} WHERE {PK}='{data['nickname']}'"))
        return msg if rtn else {"status": 500, "message": f"REQ | {table} | {msg}"}
    except Exception as e:
        return {"status": 500, "message": f"REQ | {table} | {e}"}
    
def read(db: Session, table: str = None, data: Dict = None, mode: str = "exact"):
    try:
        rtn = []
        cursor = db.execute(text(f"SELECT * FROM {table} WHERE {PK}='{data['nickname']}'"))
        for row in cursor.fetchall():
            rtn.append(dict(row))
        return {"status": 200, "message": f"REQ | {table} | {rtn}"}
    except Exception as e:
        return {"status": 500, "message": f"REQ | {table} | {e}"}