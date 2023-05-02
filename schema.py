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
    joinDate: bool
    project: str
    pm: str
    promotion: str

class Achivement(BaseModel):
    nickname: str
    content: str

class Stack(BaseModel):
    nickname: str
    stackName: str

class Outlink(BaseModel):
    nickname: str
    outLink: str


class INSERT(BaseModel):
    Nugu: Nugu

    Footprint: Footprint
    Achivement: Achivement
    Stack: Stack
    Outlink: Outlink

    # history: str # Footprint
    # joinDate: bool
    # project: str
    # pm: str
    # promotion: str

    # content: str # Achivement
    
    # stackName: str # Stack

    # outlink: str # Outlink

class HELP(BaseModel):
    Nugu: Nugu
    Footprint: Footprint
    Achivement: Achivement
    Stack: Stack
    Outlink: Outlink

SCHEMAS = [Nugu, Footprint, Achivement, Stack, Outlink, INSERT]