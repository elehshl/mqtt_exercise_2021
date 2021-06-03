import paho.mqtt.client as mqtt
import json
from random import *


class police():

    def  __init__(self, car_name, coordinaten, coor1, coor2, coor):
         self.car_name = car_name
         self.coordinaten = coordinaten
         self.coor = coor
         self.coor1 = coor1
         self.coor2 = coor2

    polices = []

    coor = [5, 2]
    coor1 = (coor[0]+randint(-2, 5))+(randint(-6, 6)/5)
    coor2 = (coor[0]+randint(-2, 5))+(randint(-6, 6)/5)
    coor1 = round(coor1, 2)
    coor2 = round(coor2, 2)
    test = [coor1, coor2]



    def on_connect(client, userdata, flags, rc):

        client.subscribe("hshl/mqtt_exercise/services/police", 2)

        client.subscribe("service/server", 2)


    def on_message(client, userdata, msg):
        print(str(msg.payload))

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("test.mosquitto.org", 1883, 60)


    data = {
     "ID": " ",
     "car_name": "police",
     "coordinaten": test,
     "topic": "hshl/mqtt_exercise/services/police"
    }

    client.publish("hshl/mqtt_exercise/services/police", json.dumps(data))   #Senden zum server

    client.loop_forever()
