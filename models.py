from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean, Double, Float
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


class Footprint(Base):
    __tablename__ = 'footprint'
    
    nickname=Column(String(length=20), ForeignKey('nugu.nickname'), primary_key=True)
    history=Column(String(length=100))
    join=Column(Boolean, default=True, nullable=not True)
    project=Column(String(length=100))
    pm=Column(String(length=20))
    promotion=Column(String(length=40))


class Achivement(Base):
    __tablename__ = 'achivement'

    nickname=Column(String(length=20), ForeignKey('nugu.nickname'), primary_key=True)
    content=Column(String(length=100), nullable=not True)


class Stack(Base):
    __tablename__ = 'stack'
    
    nickname=Column(String(length=20), ForeignKey('nugu.nickname'), primary_key=True)
    stack=Column(String(length=20), nullable=not True)


class Outlink(Base):
    __tablename__ = 'outlink'

    nickname=Column(String(length=20), ForeignKey('nugu.nickname'), primary_key=True)
    outlink=Column(String(length=100), nullable=not True)