from datetime import datetime
import uuid

def get_internal_servertime() -> datetime:
    return datetime.utcnow().time()

def get_random_uuid() -> str:
    return str(uuid.uuid4())

def sanitize(string: str) -> str:
    if not string.isalnum():
        raise ValueError("Disallowed character")
    return string

def sanitize_nickname(string: str) -> str:
    try:
        if string.isalnum():
            return string
    except:
        return None

def _make_constraints(data: dict = None):
    try:
        __constraints = []
        for key, value in data.items():
            if value != None and value != '':
                if type(value) == str:
                    __constraints.append(f"{key}='{value}'")
                elif type(value) == int:
                    __constraints.append(f"{key}={value}")
                elif type(value) == bool:
                    __constraints.append(f"{key}={value}")
        return __constraints
    except Exception as e:
        return {"status": 500, "message": f"REQ | achievement | {e}"}

def _make_like_constraints(data: dict = None):
    try:
        __constraints = []
        for key, value in data.items(): 
            if value != None and value != '':
                if type(value) == str:
                    __constraints.append(f"{key} LIKE '%{value}%'")
                elif type(value) == int:
                    __constraints.append(f"{key}={value}")
                elif type(value) == bool:
                    __constraints.append(f"{key}={value}")
        return __constraints
    except Exception as e:
        return {"status": 500, "message": f"REQ | achievement | {e}"}

def is_null(data):
    if data == None or data == '':
        return True
    return False