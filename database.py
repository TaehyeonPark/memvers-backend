# Path: workspace/memvers/memvers/database.py

from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, declarative_base
import pymysql

import getpass

pymysql.install_as_MySQLdb()

class Conn():
    HOSTNAME = ''
    PORT = '3306'
    USERNAME = 'wheel'
    DATABASE = 'memvers'
    PASSWORD = ''
    MYSQL_URL = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}'

    def __init__(self, HOSTNAME: str, PASSWORD: str, PORT: int = None, USERNAME: str = None, DATABASE: str = None):
        self.HOSTNAME = HOSTNAME
        self.PASSWORD = PASSWORD    if PASSWORD is not None else self.PASSWORD
        self.PORT = PORT            if PORT is not None else self.PORT
        self.USERNAME = USERNAME    if USERNAME is not None else self.USERNAME
        self.DATABASE = DATABASE    if DATABASE is not None else self.DATABASE

    def _url_maker(self) -> str:
        return f'mysql+pymysql://{self.USERNAME}:{self.PASSWORD}@{self.HOSTNAME}:{self.PORT}/{self.DATABASE}'
    
    def engine_maker(self) -> str:
        return create_engine(self._url_maker())

    def session_maker(self, engine) -> str:
        return sessionmaker(bind=engine)

    def base_maker(self) -> str:
        return declarative_base()
    
conn = Conn(HOSTNAME='localhost', PASSWORD=getpass.getpass('password: '))
engine = conn.engine_maker()
SessionLocal = conn.session_maker(engine)
Base = conn.base_maker()
Cursor = engine.connect().connection.cursor()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
