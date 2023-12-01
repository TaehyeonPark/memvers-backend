from fastapi.requests import Request
from inmemorydb import Redi

def IsUUIDValid(request : Request, redi : Redi) -> bool:
    __uuid = None
    try:
        __uuid = request.cookies.get("uuid")
    except:
        return False
    return True if (redi.exist(key=request.client.host) and redi.get(key=request.client.host).decode("utf-8")) == __uuid else False

def IsRequestedURLValid(request : Request, redi : Redi) -> bool:
    pass