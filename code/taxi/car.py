import paho.mqtt.client as mqtt
import json


class car():

    def  __init__(self, name, farbe):
         self.name  = name
         self.farbe = farbe

    cars = []

    def on_connect(client, userdata, flags, rc):

        client.subscribe("hshl/car/car1", 2)

        client.subscribe("taxi/server/back", 2)


    def on_message(client, userdata, msg):
        print(str(msg.payload))

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("test.mosquitto.org", 1883, 60)

    data = {
     "name": "Olga",
     "farbe": "Rot",
     "topic": "hshl/car/car1"
     }

    client.publish("hshl/car/car1", json.dumps(data))   #Senden zum server

    client.loop_forever()
