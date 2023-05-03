
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

def reader(operation="read", table="nugu", data=r_data):
    endpoint = f"http://{HOST}:{PORT}/api/v2/{operation}/{table}"
    
    formData = {
        "data": data,
        "mode": "NOT",
    }
    from json import dumps
    print(dumps(formData))
    print(formData)
    from time import time

    start = time()
    response = requests.post(endpoint, json=formData)
    # response = requests.get('http://127.0.0.1:8000/')
    end = time()
    print(f"Time=> {end-start}")
    
    print(response.json())

def index(operation="read", table="nugu", data=r_data):
    endpoint = f"http://{HOST}:{PORT}/"
    print(f"reqest : {endpoint}")
    
    from time import time

    start = time()
    response = requests.get(endpoint)
    end = time()
    print(f"Time=> {end-start}")
    
    print(response.json())



if __name__ == "__main__":
    while True:
        query = input("Query: ")
        print(query)
        if query == "exit":
            print("Bye")
            break
        elif query == '1':
            reader(operation="read", table="nugu", data=r_data)
        elif query == '2':
            index()
