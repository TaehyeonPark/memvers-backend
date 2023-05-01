# Path: workspace/memvers/memvers/crud.py
from sqlalchemy import text
from sqlalchemy.orm import Session

from typing import Dict

import models, schema
from util import Comp, Validate

PK = models.Nugu.nickname.__str__().split(".")[-1]

comp = Comp()
val = Validate(PK=PK)

def exist_nugu(db: Session, key: str = None, value: str = None):
    keys = schema.Nugu.__fields__.keys()
    if key in keys:
        try:
            db_nugu = (db.query(models.Nugu).filter(getattr(models.Nugu, key) == value).first().__dict__)
            if db_nugu:
                return True
        except Exception as e:
            pass
    return False

def get_nugu(db: Session, key: str = None, value: str = None, mode: str = "exact"):
    mode = "exact" if mode not in comp.MODES else mode
    rtn = {}
    for table in schema.SCHEMAS:
        tb_list = []
        keys = table.__fields__.keys()
        db_any = None
        try:
            if key in keys:
                db_list = []
                for db_any in db.query(getattr(models, table.__name__)).all():
                    db_any = db_any.__dict__
                    db_any.pop("_sa_instance_state")
                    if comp.comp(db_any[key], value, mode=mode):
                        db_list.append(db_any)
                if len(db_list) > 0:
                    tb_list.append(db_list)
            else:
                db_list = []
                for db_any in db.query(getattr(models, table.__name__)).all():
                    db_any = db_any.__dict__
                    db_any.pop("_sa_instance_state")
                    for key in keys:
                        if comp.comp(db_any[key], value, mode=mode):
                            db_list.append(db_any)
                if len(db_list) > 0:
                    tb_list.append(db_list)
                db_any = None
        except Exception as e:
            print(e)
        rtn[table.__name__] = tb_list
        tb_list = []
    return rtn

def insert_nugu(db: Session, nugu: schema.INSERT):
    db_any = None
    PK = nugu.Nugu.nickname

    dict_nugu = nugu.dict()
    db_nugu = models.Nugu(**dict_nugu["Nugu"])
    db.add(db_nugu)
    db.commit()
    db.refresh(db_nugu)
    tables = schema.SCHEMAS[1:-1] # Nugu, INSERT 제외

    rtn = {}

    for table in tables:
        if table.nickname == PK:
            try:
                if exist_nugu(db, key=table.nickname, value=PK):
                    rtn['fail'].append(table.__name__)
                else:
                    db_any = getattr(models, table.__name__)(**dict_nugu[table.__name__])
                    db.add(db_any)
                    db.commit()
                    db.refresh(db_any)
                    rtn['success'].append(table.__name__)
            except Exception as e:
                rtn['fail'].append(table.__name__)
                print(e)
    print(rtn)
    return rtn

def update_nugu(db: Session, nugu: schema.Nugu):
    db_list = db.query(models.Nugu).filter(models.Nugu.nickname == nugu.nickname).all()
    for db_nugu in db_list:
        for key in schema.Nugu.__fields__.keys():
            if key != models.Nugu.nickname:
                setattr(db_nugu, key, getattr(nugu, key))
        db.commit()
        db.refresh(db_nugu)
    return db_nugu