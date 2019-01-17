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

# Get the latest telemetry
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
current_dt_unix_min = current_dt_unix - 120
print("Current Time: ")
print(current_dt_unix)
print("Current Time -120s")
print(current_dt_unix_min)
print("##########")

# Get Telemetry from Past Interval
httpGetUrl = 'http://'+THINGSBOARD_HOST+'/api/plugins/telemetry/DEVICE/'+THINGSBOARD_DEVICEID+'/values/timeseries?keys='+THINGSBOARD_KEYS+'&startTs='+str(current_dt_unix_min)+'000'+'&endTs='+str(current_dt_unix)+'000'+'&interval=60000&limit=100&agg=AVG'
httpGetHeaders = {"Content-Type": "application/json", "X-Authorization": "Bearer "+jwt_token}
r3 = requests.get(httpGetUrl, headers=httpGetHeaders)
print("Status Code: " + str(r3.status_code))
telemetry_data = r3.json()
print("Telemetry Data:")
print("##########")
print(telemetry_data)
print("##########")
telemetry_data = json.loads(r3.text)
# Get the number of telemetry data
number_telemetry = telemetry_data['temperature'].length

# Load ES Configuration and Get ES Token
# Load config from JSON file
with open('ES-config.json', 'r') as h:
    config_es = json.load(h)
ES_HOST = config_es['ES_HOST']
ES_USER = config_es['ES_USER']
ES_PASSWORD = config_es['ES_PASSWORD']
ES_INDEX = config_es['ES_INDEX']
ES_TYPE = config_es['ES_TYPE']
with open('Sensor-config.json', 'r') as g:
	config_sensor = json.load(g)
sensorID = config_sensor['sensorID']
sensorLocation = config_sensor['sensorLocation']
# GET ES Token
es_httpTokenUrl = 'https://'+ES_HOST+'/_xpack/security/oauth2/token'
es_httpTokenBody = {"grant_type" : "password", "username" : ES_USER, "password" : ES_PASSWORD}
es_httpTokenHeaders = {"Content-Type": "application/json"}

r4 = requests.get(es_httpTokenUrl, data=json.dumps(es_httpTokenBody), headers=es_httpTokenHeaders)
print("Status Code: " + str(r4.status_code))
esToken_data = r4.json()
print("ES Token Data:")
print("##########")
print(esToken_data)
print("##########")
esToken_data = json.loads(r4.text)
esToken = esToken_data['access_token']

# Iterate and push each telemetry node to ES
for x in range (0, number_telemetry)
	telemetry_temperature = telemetry_data['temperature'][x]['value']
	telemetry_temperature_timestamp = telemetry_data['temperature'][x]['ts']
	print("**********")
	print("Temperature to push: " + telemetry_temperature)
	telemetry_humidity = telemetry_data['humidity'][x]['value']
	telemetry_humidity_timestamp = telemetry_data['humidity'][x]['ts']
	print("Humidity to push: "+ telemetry_humidity)
	print("**********")

	# Push to Elasticsearch
	print("**********")
	print("Pushing to Elasticsearch")
	print("**********")
	# Index Content
	es_httpIndexUrl = 'https://'+ES_HOST+'/'+ES_INDEX+'/'+ES_TYPE
	es_httpIndexBody = {"sensorID": sensorID, "sensorLocation": sensorLocation, "temperature": telemetry_temperature, "humidity": telemetry_humidity, "temperatureTimestamp": telemetry_temperature_timestamp, "humidityTimestamp": telemetry_humidity_timestamp}
	es_httpIndexHeaders = {"Content-Type": "application/json", "Authorization": "Bearer "+esToken}

	r5 = requests.put(es_httpIndexUrl, data=json.dumps(es_httpIndexBody), headers=es_httpIndexHeaders)
	print("Status Code:" + str(r5.status_code))