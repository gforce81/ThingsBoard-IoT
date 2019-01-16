import os
import time
import sys
import Adafruit_DHT as dht
import paho.mqtt.client as mqtt
import json

with open('ThingsBoard-config.json', 'r') as f:
    config = json.load(f)

# Load config from JSON file
THINGSBOARD_HOST = config['THINGSBOARD_HOST']
ACCESS_TOKEN = config['ACCESS_TOKEN']
INTERVAL = config['INTERVAL']

# THINGSBOARD_HOST = '34.199.135.198'
# ACCESS_TOKEN = 'VrafmERm8V4uOkadcQd4'

# Data capture and upload interval in seconds. Less interval will eventually hang the DHT22.
# INTERVAL=60

sensor_data = {'temperature': 0, 'humidity': 0}

next_reading = time.time() 

client = mqtt.Client()

# Set access token
client.username_pw_set(ACCESS_TOKEN)

# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
client.connect(THINGSBOARD_HOST, 1883, 60)

client.loop_start()

try:
    while True:
        humidity,temperature = dht.read_retry(dht.DHT11, 4)
        humidity = round(humidity, 2)
        temperature = round(temperature, 2)
        temperature = temperature*9
        temperature = temperature/5
        temperature = temperature + 32
        print(u"Temperature: {:g}\u00b0F, Humidity: {:g}%".format(temperature, humidity))
        sensor_data['temperature'] = temperature
        sensor_data['humidity'] = humidity

        # Sending humidity and temperature data to ThingsBoard
        client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)

        next_reading += INTERVAL
        sleep_time = next_reading-time.time()
        if sleep_time > 0:
            time.sleep(sleep_time)
except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()