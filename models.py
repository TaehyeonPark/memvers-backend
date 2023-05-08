from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean, Float
from sqlalchemy.orm import relationship, backref, declarative_base

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


class Footprint():
    __tablename__ = 'footprint'
    
    nickname=Column(String(length=20), nullable=not True)
    history=Column(String(length=100))
    joinDate=Column(Boolean, default=True, nullable=not True)
    project=Column(String(length=100))
    pm=Column(String(length=20))
    promotion=Column(String(length=40))


class Achivement():
    __tablename__ = 'achivement'

    nickname=Column(String(length=20), nullable=not True)
    content=Column(String(length=100), nullable=not True)


class Stack():
    __tablename__ = 'stack'
    
    nickname=Column(String(length=20), nullable=not True)
    stackName=Column(String(length=20), nullable=not True)


class Outlink():
    __tablename__ = 'outlink'

    nickname=Column(String(length=20), nullable=not True)
    outLink=Column(String(length=100), nullable=not True)

class Project():
    __tablename__ = 'project'

    nickname=Column(String(length=20), nullable=not True)
    project=Column(String(length=20), nullable=not True)
    current=Column(Boolean, default=True, nullable=not True)

ORMS = [Nugu, Footprint, Achivement, Stack, Outlink, Project]
TABLES = [table.__tablename__ for table in ORMS]
# TABLES = ['nugu', 'footprint', 'achivement', 'stack', 'outlink']
KEYS = [{ORM.__tablename__ : [key for key in ORM.__dict__.keys() if not key.startswith('_')]} for ORM in ORMS]
# KEYS = [
#   {'nugu': ['nickname', 'studentId', 'email', 'phoneNum', 'manager', 'dongbang', 'birthday', 'developer', 'designer', 'wheel', 'rnk', 'hide']},
#   {'footprint': ['nickname', 'history', 'joinDate', 'project', 'pm', 'promotion']},
#   {'achivement': ['nickname', 'content']}, {'stack': ['nickname', 'stackName']},
#   {'outlink': ['nickname', 'outLink']},
#   {'project': ['nickname', 'project', 'current']}
# ]