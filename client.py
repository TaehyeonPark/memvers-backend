import requests

def nugu_create_post():
    end_point = "http://127.0.0.1:8000/api/v1/nugu/create"
    # response_model=schema.Nugu
    data = {
        "nickname": "source",
        "studentId": "20230303",
        "email": "",
        "phoneNum": "01036800697",
        "manager": False,
        "dongbang": False,
        "birthday": "20040113",
        "developer": True,
        "designer": False,
        "wheel": False,
        "rnk": 0,
        "hide": False,
    }

    response = requests.post(url=end_point, data=data)
    print(response.text)

def nugu_create_get():
    end_point = "http://127.0.0.1:8000/api/v1/nugu/create"
    data = {
        "nickname": "source",
        "studentId": "20230303",
        "email": "",
        "phoneNum": "01036800697",
        "manager": False,
        "dongbang": False,
        "birthday": "20040113",
        "developer": True,
        "designer": False,
        "wheel": False,
        "rnk": 0,
        "hide": False,
    }

    response = requests.get(url=end_point, params=data)
    print(response.text)


if __name__ == "__main__":
    nugu_create_get()