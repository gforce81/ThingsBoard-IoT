import os
import time
import sys
import json
import requests


with open('ThingsBoard-config.json', 'r') as f:
    config = json.load(f)
# Load config from JSON file
THINGSBOARD_HOST = config['THINGSBOARD_HOST']
THINGSBOARD_USERNAME = config['THINGSBOARD_USERNAME']
THINGSBOARD_PASSWORD = config['THINGSBOARD_PASSWORD']

# Get the JWT token
httpPostUrl = 'http://'+THINGSBOARD_HOST+'/api/auth/login?Content-Type=application/json&Accept=application/json'
httpPostBody = {"username": THINGSBOARD_USERNAME, "password": THINGSBOARD_PASSWORD}
httpPostHeathers = {"Content-Type": "application/json"}
r = requests.post(httpPostUrl, data=json.dumps(httpPostBody), headers=httpPostHeathers)
print("Status Code: " + str(r.status_code))
jwt_data = json.loads(r.text)
print("JWT Token:")
print("##########")
print(jwt_data)
print("##########")