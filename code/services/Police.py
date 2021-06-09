import paho.mqtt.client as mqtt
import json
from random import *
BROKER_ADDRESS = "test.mosquitto.org"
PORT = 1883
import time
id = ""
name = ""



print("gib einen namen ein:")
name = input()

def send(topic, object):
    client = mqtt.Client("client")
    client.connect(BROKER_ADDRESS, PORT)
    name = object
    print("Police")
    def __init__(self, name):
            self.name = name
    print(" SEND Connected to MQTT Broker: " + BROKER_ADDRESS)
    msg = str(name)
    print(msg)
    client.publish(topic, msg)
    client.loop()

def receive():
    global id
    temp = []
    client = mqtt.Client("user")
    client.connect(BROKER_ADDRESS, PORT)
    def on_message(client, userdata, message):
        msg = str(message.payload.decode("utf-8"))
        print("message received: ", msg)
        print("message topic: ", message.topic)
        print(msg)
        temp =  [message.topic,msg]
        processing(temp)


    def on_connect(client, userdata, flags, rc):
        print("receive Connected to MQTT Broker: " + BROKER_ADDRESS)
        client.subscribe("hshl/mqtt_exercise/services/police/back",2)
        client.subscribe("hshl/mqtt_exercise/services/police/"+str(id)+"/order/back", 2)

    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_start()
    time.sleep(5)
    client.loop_stop()

def processing(array):
    global id
    js = json.loads(array[1])
    if "hshl/mqtt_exercise/services/police/back" == array[0] and str(js['name']) == str(name):
        id = js['id']


zahly = randint(0, 4)
zahlx = randint(0, 4)
coordinates = str(zahly)+";"+str(zahlx)


def registration():
    global name
    data = {
    "id": "register",
    "name": name,
    "coordinates": coordinates
    }
    send("hshl/mqtt_exercise/services/police", json.dumps(data))
    receive()

registration()
