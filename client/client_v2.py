
import requests

c_data = {
    "nickname": "source",
    "studentId": "20000101",
    "email": "",
    "phoneNum": "01012345678",
    "manager": False,
    "dongbang": False,
    "birthday": "20040101",
    "developer": True,
    "designer": False,
    "wheel": False,
    "rnk": 0,
    "hide": False,
}
r_data = {
    "key": "nickname",
    "value": "source",
}

def create(nickname="source", table="nugu", data=c_data):
    endpoint = f"http://localhost:8000/api/v2/{nickname}/{table}/create"
    response = requests.post(endpoint, json=data)
    print(response.json())
    
if __name__ == "__main__":
    create()