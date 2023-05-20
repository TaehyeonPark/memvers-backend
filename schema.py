# Path: workspace/memvers/memvers/schema.py

from pydantic import BaseModel
from typing import List, Dict, Any, Union, Optional

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
    content: str

class Achievement(BaseModel):
    nickname: str
    content: str

class Stack(BaseModel):
    nickname: str
    stack: str

class Outlink(BaseModel):
    nickname: str
    outlink: str

class Project(BaseModel):
    nickname: str
    project: str
    current: bool

class INSERT(BaseModel):
    Nugu: Nugu

    Footprint: Footprint
    Achievement: Achievement
    Stack: Stack
    Outlink: Outlink


class HELP(BaseModel):
    Nugu: Nugu
    Footprint: Footprint
    Achievement: Achievement
    Stack: Stack
    Outlink: Outlink

class READ(BaseModel):
    data: Dict[str, Any]
    mode: str


SCHEMAS = [Nugu, Footprint, Achievement, Stack, Outlink, INSERT]
