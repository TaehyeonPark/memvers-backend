
import requests

HOST = "localhost"
PORT = 8000

c_data = {
    "nickname": "source",
    "studentId": "20000101",
    "email": "",
    "phoneNum": "0000000000",
    "manager": False,
    "dongbang": False,
    "birthday": "20040101",
    "developer": True,
    "designer": False,
    "wheel": False,
    "rnk": 0,
    "hide": False,
}
c_achivement_dummy = {
    "nickname": "source",
    "content": "dummy2",
}

r_data = {
    "nickname": "source",
}

def operator(operation="insert", table="nugu", data=c_achivement_dummy):
    endpoint = f"http://{HOST}:{PORT}/api/v2/{operation}/{table}"
    response = requests.post(endpoint, json=data)
    print(response.json())

if __name__ == "__main__":
    operator('read', 'achivement', r_data)