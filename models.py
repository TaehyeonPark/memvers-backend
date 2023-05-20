from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean, Float, BOOLEAN
from sqlalchemy.orm import relationship, backref, declarative_base

from util import is_null 

Base = declarative_base()

class Nugu(Base):
    __tablename__ = 'nugu'

    nickname=Column(String(length=20), primary_key=True)
    studentId=Column(String(length=20), nullable=not True)
    email=Column(String(length=100), unique=True)
    phoneNum=Column(String(length=11), unique=True)
    manager=Column(Boolean, default=False, nullable=not True)
    dongbang=Column(Boolean, default=False, nullable=not True)
    birthday=Column(Integer)
    developer=Column(Boolean, default=False, nullable=not True)
    designer=Column(Boolean, default=False, nullable=not True)
    wheel=Column(Boolean, default=False, nullable=not True)
    rnk=Column(Integer, default=0, nullable=not True) # 0: 준회원 1: 정회원 2: 명예회원
    hide=Column(Boolean, default=True, nullable=not True)

    def __type__():
        return {"nickname": str, "studentId": str, "email": str, "phoneNum": str, "manager": bool, "dongbang": bool, "birthday": int, "developer": bool, "designer": bool, "wheel": bool, "rnk": int, "hide": bool}

class Footprint():
    __tablename__ = 'footprint'
    
    nickname=Column(String(length=20), nullable=not True)
    history=Column(String(length=100), nullable=not True)
    content=Column(String(length=100), nullable=not True)
    def __type__():
        return {"nickname": str, "history": str, "content": str}
    
class Achievement():
    __tablename__ = 'achievement'

    nickname=Column(String(length=20), nullable=not True)
    content=Column(String(length=100), nullable=not True)

    def __type__():
        return {"nickname": str, "content": str}

class Stack():
    __tablename__ = 'stack'
    
    nickname=Column(String(length=20), nullable=not True)
    stack=Column(String(length=20), nullable=not True)

    def __type__():
        return {"nickname": str, "stack": str}
    
class Outlink():
    __tablename__ = 'outlink'

    nickname=Column(String(length=20), nullable=not True)
    outlink=Column(String(length=100), nullable=not True)

    def __type__():
        return {"nickname": str, "outlink": str}

class Project():
    __tablename__ = 'project'

    nickname=Column(String(length=20), nullable=not True)
    project=Column(String(length=20), nullable=not True)
    current=Column(Boolean, default=True, nullable=not True)

    def __type__():
        return {"nickname": str, "project": str, "current": bool}


ORMS = [Nugu, Footprint, Achievement, Stack, Outlink, Project]
ORMS_DICT = {ORM.__tablename__ : ORM for ORM in ORMS}
TABLES = [table.__tablename__ for table in ORMS]
KEYS = [{ORM.__tablename__ : [key for key in ORM.__dict__.keys() if not key.startswith('_')]} for ORM in ORMS]
TYPES = [{ORM.__tablename__ : ORM.__type__()} for ORM in ORMS]


def get_keys_from_table(table : str) -> list:
    return KEYS[TABLES.index(table)][table]

def get_types_from_table(table : str) -> dict:
    return TYPES[TABLES.index(table)][table]

def yield_default_value_type_by_key(table : str, key : str) -> type:
    __type = get_types_from_table(table)[key]
    if __type == str:
        return ""
    elif __type == int:
        return 0
    elif __type == float:
        return 0.0
    elif __type == bool:
        return False
    else:
        return None
    
def type_casting_by_table(table: str, key: str, data) -> type:
    __type = get_types_from_table(table)[key]
    if __type == str:
        return str(data)
    elif __type == int:
        if type(data) == str:
            if data.isdigit():
                return int(data)
            else:
                return 0
        else:
            return int(data)
    elif __type == float:
        if type(data) == str:
            if data.isdigit():
                return float(data)
            else:
                return 0.0
        else:
            return float(data)
    elif __type == bool:
        if type(data) == str:
            if 'false' in data.lower():
                return False
            elif 'true' in data.lower():
                return True
        elif type(data) == int:
            if data == 0:
                return False
            elif data == 1:
                return True
        elif type(data) == bool:
            return data
        elif type(data) == None:
            return False
        else:
            return None
    else:
        return None