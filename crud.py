# Path: workspace/memvers/memvers/crud.py
from sqlalchemy import text
from sqlalchemy.orm import Session

import models, schema
from util import Comp

comp = Comp()

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
    print(f"mode: {mode}")
    print("*" * 50)
    keys = schema.Nugu.__fields__.keys()
    db_nugu = None

    if key in keys:
        db_list = []
        for db_nugu in db.query(models.Nugu).all():
            db_nugu = db_nugu.__dict__
            db_nugu.pop("_sa_instance_state")
            if comp.comp(db_nugu[key], value, mode=mode):
                # return db_nugu
                db_list.append(db_nugu)
        if len(db_list) > 0:
            return db_list
    else:
        db_list = []
        for db_nugu in db.query(models.Nugu).all():
            db_nugu = db_nugu.__dict__
            db_nugu.pop("_sa_instance_state")
            for key in keys:
                if comp.comp(db_nugu[key], value, mode=mode):
                    db_list.append(db_nugu)
        if len(db_list) > 0:
            return db_list
        db_nugu = None
    return db_nugu

def insert_nugu(db: Session, nugu: schema.Nugu):
    db_nugu = models.Nugu(**nugu.dict())
    db.add(db_nugu)
    db.commit()
    db.refresh(db_nugu)
    return db_nugu

def update_nugu(db: Session, nugu: schema.Nugu):
    db_list = db.query(models.Nugu).filter(models.Nugu.nickname == nugu.nickname).all()
    for db_nugu in db_list:
        for key in schema.Nugu.__fields__.keys():
            if key != models.Nugu.nickname:
                setattr(db_nugu, key, getattr(nugu, key))
        db.commit()
        db.refresh(db_nugu)

    return db_nugu