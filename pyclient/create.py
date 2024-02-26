import requests
from getpass import getpass

data =  {
    "title": "Welcome Amalia",
    "price": 100.99,
}
auth_endpoint = "http://localhost:8000/api/auth/"
username = input("What's is your username")
password = getpass("What's is your password")
auth_response = requests.post(auth_endpoint, json={"username":username,"password":password}) 
print(auth_response.json()['token'])

if auth_response.status_code == 200:
    token = auth_response.json()['token']
    headers = {
        "Authorization": f'Bearer {token}'
    }
    endpoint = "http://localhost:8000/api/products/"

    get_response = requests.post(endpoint,headers=headers,json=data) 
    print(get_response)
