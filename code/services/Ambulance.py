import paho.mqtt.client as mqtt
import json
from random import *


class ambulance():

    def  __init__(self, car_name, coordinaten):
         self.car_name = car_name
         self.coordinaten = coordinaten

    ambulances = []



    def on_connect(client, userdata, flags, rc):

        client.subscribe("hshl/mqtt_exercise/services/ambulance", 2)

        client.subscribe("service/server", 2)


    def on_message(client, userdata, msg):
        print(str(msg.payload))

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("test.mosquitto.org", 1883, 60)
    
    zahly = randint(0, 4)
    zahlx = randint(0, 4)
    coordinates = str(zahly)+";"+str(zahlx)

    data = {
     "ID": " ",
     "car_name": "firefighter",
     "coordinaten": coordiantes,
     "topic": "hshl/mqtt_exercise/services/ambulance"
    }

    client.publish("hshl/mqtt_exercise/services/ambulance", json.dumps(data))   #Senden zum server

    client.loop_forever()
