import paho.mqtt.client as mqtt
import json
from random import *


class police():

    def  __init__(self, car_name, coordinaten, coor1, coor2, coor):
         self.car_name = car_name
         self.coordinates = coordinates


    polices = []
    
    def processing(msg):
        global id
        global idCar
        global count
        data = ""
        Abfrage = 1
        print(msg[1])
        #die erhaltene id verarbeiten
        js = json.loads(msg[1])
        if msg[0]=="hshl/mqtt_exercise/police/back" and js['name'] == "Dan":
            id = js['id']
            print(id)
            pass
        elif msg[0] == "hshl/mqtt_exercise/set_position":
            storePosition(js["id"],js["type"],js["coordinates"])

    def requestPosition(idCar,type):
        name =""
        for i in range(0,len(type)):
            pass
        data ={
        "id":idCar,
        "name": name
        }
        send(data,"hshl/exercise/get_position")

    def getid():
      data = {
       "id": "register",
       "name": "Dan",
       "coordinates": coordinates
       }
      send(json.dumps(data),"hshl/mqtt_exercise/user")
      receive()

    def on_connect(client, userdata, flags, rc):

        client.subscribe("hshl/mqtt_exercise/services/police", 2)

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
     "id": " ",
     "car_name": "Police",
     "coordinaten": coordinates,
     "topic": "hshl/mqtt_exercise/services/police"
    }

    client.publish("hshl/mqtt_exercise/services/police", json.dumps(data))   #Senden zum server

    client.loop_forever()
