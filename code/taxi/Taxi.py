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


    zahly = randint(0, 4)
    zahlx = randint(0, 4)
    coordinates = str(zahly)+"."+str(zahlx)
    #data = {
    # "name": "Taxi",
    ## "cordinaten": coordinates,
    # "topic": "hshl/mqtt_exercise/taxi"
    # }
    temp = ["Id1", "taxischmitt" ,str(coordinates)]
    data= ""
    for i in range(0,len(temp)):
        if i != 0:
            data += ","
        data += temp[i]
    client.publish("hshl/mqtt_exercise/taxi", data)#json.dumps(data))   #Senden zum server

    client.loop_forever()
