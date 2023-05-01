
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

def nugu_create_post():
    end_point = "http://127.0.0.1:8000/api/v1/nugu/create"
    response = requests.post(url=end_point, data=c_data)
    print(response.text)

def nugu_create_get():
    end_point = "http://127.0.0.1:8000/api/v1/nugu/create"
    response = requests.get(url=end_point, params=c_data)
    print(response.text)

def nugu_read_post():
    end_point = "http://127.0.0.1:8000/api/v1/nugu/read"
    response = requests.post(url=end_point, data=r_data)
    print(response.text)

if __name__ == "__main__":
    nugu_read_post()