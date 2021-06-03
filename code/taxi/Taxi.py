import paho.mqtt.client as mqtt
import json
from random import *

class car():

    def  __init__(self, name, coordinaten,zahl):
         self.name  = name
         self.coordinaten = coordinaten
         self.zahl = zahl

    cars = []

    def on_connect(client, userdata, flags, rc):

        client.subscribe("hshl/mqtt_exercise/taxi", 2)

        client.subscribe("hshl/mqtt_exercise/server", 2)


    def on_message(client, userdata, msg):
        print(str(msg.payload))

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("test.mosquitto.org", 1883, 60)


    zahl = 150 + randint(1, 10)

    data = {
     "name": "Taxi",
     "cordinaten": zahl,
     "topic": "hshl/mqtt_exercise/taxi"
     }

    client.publish("hshl/mqtt_exercise/taxi", json.dumps(data))   #Senden zum server

    client.loop_forever()
