from sqlalchemy import text
from sqlalchemy.orm import Session
import pymysql

from typing import Dict, List, Tuple, Any, Union

import models, schema

import util

PK = models.Nugu.nickname.__str__().split(".")[-1]
HANDLER = ["create", "read", "update"]

def _execute(db: Session, query: str = None):
    try:
        cursor = db.execute(query)
        db.commit()
        if cursor.  rowcount > 0:
            return True, {"status": 200, "message": f"REQ | Successfully executed"}
        return False, {"status": 400, "message": f"REQ | Failed to execute"}
    except Exception as e:
        return False, e

def insert(db: Session, table: str = None, data: Dict = None):
    try:
        sorted_data = {}
        for key in models.get_keys_from_table(table=table):
            sorted_data[key] = data[key]
        
        if type(read(db=db, table=table, data=sorted_data)) == list and len(read(db=db, table=table, data=sorted_data)) > 0: # duplicate check
            return False
        print(f"INSERT INTO {table} VALUES {tuple(sorted_data.values())}")
        rtn, msg = _execute(db=db, query=text(f"INSERT INTO {table} VALUES {tuple(sorted_data.values())}"))
        return rtn
    except Exception as e:
        return False
    finally:
        db.close()

def delete(db: Session, table: str = None, data: Dict = None):
    try:
        sorted_data = {}
        for key in models.get_keys_from_table(table=table):
            sorted_data[key] = data[key]
        # __constraints = [f"{key}='{value}'" for key, value in sorted_data.items() if value != None and value != '']
        __constraints = util._make_constraints(data=sorted_data)
        print(f"DELETE FROM {table} WHERE {' AND '.join(__constraints)}")
        rtn, msg = _execute(db=db, query=text(f"DELETE FROM {table} WHERE {' AND '.join(__constraints)}"))
        return rtn
    except Exception as e:
        return False
    finally:
        db.close()

def update(db: Session, table: str = None, data: Dict = None): # Needed: Different edition level by privilige.
    try:
        sorted_data = {}
        for key in models.get_keys_from_table(table=table):
            sorted_data[key] = data[key]
        print(f"UPDATE {table} SET {', '.join(sorted_data)} WHERE {' AND '.join(util._make_constraints(data=sorted_data))}")
        rtn, msg = _execute(db=db, query=text(f"UPDATE {table} SET {', '.join(sorted_data)} WHERE {' AND '.join(util._make_constraints(data=sorted_data))}"))
        return msg if rtn else {"status": 500, "message": f"REQ | {table} | {msg}"}
    except Exception as e:
        return {"status": 500, "message": f"REQ | {table} | {e}"}
    finally:
        db.close()

def edit(db: Session, table: str = None, olddata: dict = None, newdata: dict = None):
    try:
        newsorted_data = {}
        for key in models.get_keys_from_table(table=table):
            newsorted_data[key] = newdata[key]
        oldsorted_data = {}
        for key in models.get_keys_from_table(table=table):
            oldsorted_data[key] = olddata[key]
        if type(read(db=db, table=table, data=newsorted_data)) == list and len(read(db=db, table=table, data=newsorted_data)) > 0: # duplicate check
            return False
        print(f"UPDATE {table} SET {', '.join(util._make_constraints(data=newsorted_data))} WHERE {' AND '.join(util._make_constraints(data=oldsorted_data))}")
        rtn, msg = _execute(db=db, query=text(f"UPDATE {table} SET {', '.join(util._make_constraints(data=newsorted_data))} WHERE {' AND '.join(util._make_constraints(data=oldsorted_data))}"))
        print(rtn, msg)
        return rtn
    except Exception as e:
        return False
    finally:
        db.close()

def search(db: Session, table: str = None, key: str = PK, data: str = None, mode: str = "OR") -> Union[List[Dict], Dict]:
    try:
        rtn = []
        cursor = None
        if mode == "EXACT":
            cursor = db.execute(text(f"SELECT * FROM {table} WHERE {key}='{data}' ORDER BY {PK}"))
        elif mode == "AND":
            __constraints = [f"{key}='{value}'" for key, value in data.items() if value != None and value != '']
            cursor = db.execute(text(f"SELECT * FROM {table} WHERE {' AND '.join(__constraints)} ORDER BY {PK}"))
        elif mode == "OR":
            cursor = db.execute(text(f"SELECT * FROM {table} WHERE {key} LIKE '%{data}%' ORDER BY {PK}"))
        elif mode == "XOR":
            cursor = db.execute(text(f"SELECT * FROM {table} WHERE {' XOR '.join(data)} ORDER BY {PK}"))
        elif mode == "NOT":
            cursor = db.execute(text(f"SELECT * FROM {table} WHERE NOT {' AND NOT '.join(data)} ORDER BY {PK}"))
        else:
            return {"status": 400, "message": f"REQ | {table} | Invalid mode", "data": None}
        
        db.commit()
        
        for row in cursor.fetchall():
            rtn.append(dict(row))
        
        return rtn
    
    except Exception as e:
        return {"status": 500, "message": f"REQ | {table} | {e}"}
    finally:
        db.close()


def read(db: Session, table: str = None, data: Dict = None, mode: str = "AND") -> dict:
    try:
        rtn = []
        cursor = None

        if mode == "EXACT":
            cursor = db.execute(text(f"SELECT * FROM {table} WHERE {' AND '.join(util._make_constraints(data=data))} ORDER BY {PK}"))
        elif mode == "LIKE":
            cursor = db.execute(text(f"SELECT * FROM {table} WHERE {' OR '.join(util._make_like_constraints(data=data))} ORDER BY {PK}"))
        elif mode == "AND":
            cursor = db.execute(text(f"SELECT * FROM {table} WHERE {' AND '.join(util._make_constraints(data=data))} ORDER BY {PK}"))
        elif mode == "OR":
            cursor = db.execute(text(f"SELECT * FROM {table} WHERE {' OR '.join(util._make_constraints(data=data))} ORDER BY {PK}"))
        elif mode == "XOR":
            cursor = db.execute(text(f"SELECT * FROM {table} WHERE {' XOR '.join(data)} ORDER BY {PK}"))
        elif mode == "NOT":
            cursor = db.execute(text(f"SELECT * FROM {table} WHERE NOT {' AND NOT '.join(data)} ORDER BY {PK}"))
        else:
            return {"status": 400, "message": f"REQ | {table} | Invalid mode", "data": None}
        
        db.commit()
        
        for row in cursor.fetchall():
            rtn.append(dict(row))
        return rtn
    
    except Exception as e:
        return {"status": 500, "message": f"REQ | {table} | {e}"}
    finally:
        db.close()