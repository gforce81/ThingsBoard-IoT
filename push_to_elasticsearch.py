import os
import time
import sys
import json
import requests
import calendar
import datetime


with open('ThingsBoard-config.json', 'r') as f:
    config = json.load(f)
# Load config from JSON file
THINGSBOARD_HOST = config['THINGSBOARD_HOST']
THINGSBOARD_USERNAME = config['THINGSBOARD_USERNAME']
THINGSBOARD_PASSWORD = config['THINGSBOARD_PASSWORD']
THINGSBOARD_DEVICEID = config['THINGSBOARD_DEVICEID']
THINGSBOARD_KEYS = config['THINGSBOARD_KEYS']

# Get the JWT token
httpPostUrl = 'http://'+THINGSBOARD_HOST+'/api/auth/login?Content-Type=application/json&Accept=application/json'
httpPostBody = {"username": THINGSBOARD_USERNAME, "password": THINGSBOARD_PASSWORD}
httpPostHeathers = {"Content-Type": "application/json"}
r = requests.post(httpPostUrl, data=json.dumps(httpPostBody), headers=httpPostHeathers)
print("Status Code: " + str(r.status_code))
jwt_data = r.json()
print("JWT Token:")
print("##########")
print(jwt_data)
print("##########")
jwt_data = json.loads(r.text)
jwt_token = jwt_data['token']

# Get the latest telemtry
httpGetUrl = 'http://'+THINGSBOARD_HOST+'/api/plugins/telemetry/DEVICE/'+THINGSBOARD_DEVICEID+'/values/timeseries?keys='+THINGSBOARD_KEYS
httpGetHeaders = {"Content-Type": "application/json", "X-Authorization": "Bearer "+jwt_token}
r2 = requests.get(httpGetUrl, headers=httpGetHeaders)
print("Status Code: " + str(r2.status_code))
telemetry_data = r2.json()
print("Telemetry Data:")
print("##########")
print(telemetry_data)
print("##########")

# Get time
current_dt = datetime.datetime.utcnow()
current_dt_unix = calendar.timegm(current_dt.utctimetuple())
print(current_dt_unix)
