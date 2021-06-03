import paho.mqtt.client as mqtt
import json
from random import *





class firefighter():

    def  __init__(self, car_name, coordinaten):
         self.car_name = car_name
         self.coordinaten = coordinaten

    firefighters = []



    def on_connect(client, userdata, flags, rc):

        client.subscribe("hshl/mqtt_exercise/services/firefighter", 2)

        client.subscribe("service/server", 2)


    def on_message(client, userdata, msg):
        print(str(msg.payload))

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("test.mosquitto.org", 1883, 60)


    data = {
     "ID": " ",
     "car_name": "firefighter",
     "coordinaten": " ",
     "topic": "hshl/mqtt_exercise/services/firefighter"
    }

    client.publish("hshl/mqtt_exercise/services/firefighter", json.dumps(data))   #Senden zum server

    client.loop_forever()
