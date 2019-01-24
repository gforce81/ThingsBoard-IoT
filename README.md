# Pushing sensor data (temperature & humidity) to ThingsBoard and to Elasticsearch

This (sample) project does 2 things:
* Pushes sensor data (DHT11 - temperature & humidity) to ThingsBoard
* Queries ThingsBoard regularly (via Cron job) to update an Elasticsearch index for data visualization using Kibana & Timelion

## Setup

### Requirements
* Raspberry Pi 3
* DHT11 Temperature & Humidity sensor
* ThingsBoard deployment (local or cloud)
* Elasticsearch and Kibana (local or cloud)

### Steps

#### ThingsBoard
* Log into your ThingsBoard environment
* Go to "Devices" and click "+"
* Name your device (e.g.: DHT11-device1)
* Once the device is created, go to **Manage Credentials** and copy the **Access Token**

#### Elasticsearch
* Create an Elasticsearch index using the schema provided in *ES_schema.json*

#### Raspberri Pi 
* Connect the DHT11 to your Raspberry Pi 3
```
  DHT11 Data -> Raspberry PI GPIO 2
  DHT11 VCC -> Raspberry Pi 5V
  DHT11 GND -> Raspberry Pi GND
 ```
* clone this repository to your Raspberry Pi 3
``` 
  git clone https://github.com/gforce81/ThingsBoard-IoT.git
``` 
* install MQTT
```
  sudo pip install paho-mqtt
 ```
* update all the **-config.json** files to match your environments
* clone the Adafruit repository for the DHT11 https://github.com/adafruit/DHT-sensor-library
```
  git clone https://github.com/adafruit/Adafruit_Python_DHT.git
  cd Adafruit_Python_DHT
  sudo python setup.py install
 ```
 * Add the commands included in the **cron_jab.tx** file to your Crontab
 * Reload Cron: 
 ```
  sudo service cron reload
 ```
 * Start the telemetry gathering
 ```
  python mqtt-dht11.py
 ```
 
 #### Dashboarding
 * Head over to your Kibana instance
 * Select Timelion
 * Use the following query
 ```
  .es(index=thingsboard, timefield=temperatureTimestamp, metric=avg:temperature)
     .color(#ff0000)
     .points(radius=6, fill=1, fillColor=#009900)
 ```



