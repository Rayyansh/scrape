import requests

# set the login url and form data
url = "https://kite.zerodha.com/api/login"
data = {
    "user_id": "abdc",
    "password": "abcd3214"
}

# send the POST request to the login endpoint
response = requests.post(url, data=data)

# print the response
print(response.text)