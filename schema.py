# Path: workspace/memvers/memvers/schema.py

from pydantic import BaseModel

class Nugu(BaseModel):
    nickname: str
    studentId: str
    email: str
    phoneNum: str
    manager: bool
    dongbang: bool
    birthday: int
    developer: bool
    designer: bool
    wheel: bool
    rnk: int
    hide: bool

class Footprint(BaseModel):
    nickname: str
    history: str
    join: bool
    project: str
    pm: str
    promotion: str

class Achivement(BaseModel):
    nickname: str
    content: str

class Stack(BaseModel):
    nickname: str
    stack: str

class Outlink(BaseModel):
    nickname: str
    outlink: str
