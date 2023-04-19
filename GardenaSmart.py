#!/usr/bin/python3 -u
import websocket
from threading import Thread
import time
import sys
import os
import requests
import json
import paho.mqtt.client as mqtt

# account specific values
USERNAME = 'yourGardenaUserName'
PASSWORD = 'YourGardenaPassword'
API_KEY = 'yourGardenaAPIKey'
#MQTT Broker
BROKER = 'BrokerIP'
BROKER_PORT = 1883
BROKER_USER = 'ifApplicable'
BROKER_PW = 'ifApplicable'
# other constants
AUTHENTICATION_HOST = 'https://api.authentication.husqvarnagroup.dev'
SMART_HOST = 'https://api.smart.gardena.dev'

AUTH_TOKEN =''






class Client:
    def on_message(self, any, message):
        #print("msg", message)

        mclient.publish('Gardena/out', message)

    def on_error(self, error, any):
        print("error", error)
        time.sleep(60)
        os.system("sudo service gardena restart") #please adjust, if your service has a differnt name

    def on_close(self):
        print("### Gardena WS closed ###")
        self.live = False
        sys.exit(0)


    
    def on_ping():
        print("Gardena ping")

    def on_pong():
        print("Gardena pong")
        
    def on_open(self, any):
        print("### connected ###")



        self.live = True

        def run(*args):
            while self.live:
                time.sleep(1)

        Thread(target=run).start()


class mqttClient:

    def on_close(self):
        self.live = False
        print("### Gardena MQTT disconnected ###")
        sys.exit(0)

    def on_message(client, userdata, any, message):
        #print('mqtt_in', message.payload)
        jsPayload = json.loads(message.payload)
        jdata = jsPayload['data']
        ServiceID = jdata['id']
        headers = {
        "Content-Type": "application/vnd.api+json",
        "x-api-key": API_KEY,
        "Authorization-Provider": "husqvarna",
        "Authorization": "Bearer " + AUTH_TOKEN}
        url = "https://api.smart.gardena.dev/v1/command/" + ServiceID
        response = requests.put(url, data=message.payload, headers=  headers)

        print(response)
    



if __name__ == "__main__":
    payload = {'grant_type': 'password', 'username': USERNAME, 'password': PASSWORD,
               'client_id': API_KEY}

    print("Logging into authentication system...")
    r = requests.post(f'{AUTHENTICATION_HOST}/v1/oauth2/token', data=payload)
    assert r.status_code == 200, r
    auth_token = r.json()["access_token"]
    AUTH_TOKEN = auth_token
   
    

    headers = {
        "Content-Type": "application/vnd.api+json",
        "x-api-key": API_KEY,
        "Authorization-Provider": "husqvarna",
        "Authorization": "Bearer " + auth_token
    }

    r = requests.get(f'{SMART_HOST}/v1/locations', headers=headers)
    assert r.status_code == 200, r
    assert len(r.json()["data"]) > 0, 'location missing - user has not setup system'
    location_id = r.json()["data"][0]["id"]

    payload = {
        "data": {
            "type": "WEBSOCKET",
            "attributes": {
                "locationId": location_id
            },
            "id": "does-not-matter"
        }
    }
    print("Logged in (%s), getting WebSocket ID..." % auth_token)
    r = requests.post(f'{SMART_HOST}/v1/websocket', json=payload, headers=headers)

    assert r.status_code == 201, r
    print("WebSocket ID obtained, connecting...")
    response = r.json()
    websocket_url = response["data"]["attributes"]["url"]

    #websocket.enableTrace(True)

    mclient = mqtt.Client('Gardena')
    mclient.username_pw_set(BROKER_USER,BROKER_PW)
    mclient.connect(BROKER,BROKER_PORT)
    
    mclient.subscribe('Gardena/in')
    
    mclient.loop_start()
    #

    client = Client()
    MqttClient = mqttClient()
    mclient.on_message=MqttClient.on_message
    
    websocket.setdefaulttimeout(150)
    ws = websocket.WebSocketApp(
        websocket_url,
        on_message=client.on_message,
        on_error=client.on_error,
        on_close=client.on_close,
        on_ping=client.on_ping,
        on_pong=client.on_pong)
    ws.on_open = client.on_open
    
    ws.run_forever(ping_interval=150, ping_timeout=10)
    
    
    
   
