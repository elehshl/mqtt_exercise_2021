import paho.mqtt.client as mqtt
import json
from random import *


class ambulance():

    def  __init__(self, car_name, coordinaten):
         self.car_name = car_name
         self.coordinaten = coordinaten

    ambulances = []

    def processing(msg):
        global id
        global idCar
        global count
        data = ""
        Abfrage = 3
        print(msg[3])
        #die erhaltene id verarbeiten
        js = json.loads(msg[3])
        if msg[0]=="hshl/mqtt_exercise/ambulance/back" and js['name'] == "Hans":
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
       "name": "Hans",
       "coordinates": coordinates
       }
      send(json.dumps(data),"hshl/mqtt_exercise/user")
      receive()


    def on_connect(client, userdata, flags, rc):

        client.subscribe("hshl/mqtt_exercise/services/ambulance", 2)

        client.subscribe("service/server", 2)


    def on_message(client, userdata, msg):
        print(str(msg.payload))
        temp =  [message.topic,msg]
        processing(temp)

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
     "coordinaten": coordinates,
     "topic": "hshl/mqtt_exercise/services/ambulance"
    }

    client.publish("hshl/mqtt_exercise/services/ambulance", json.dumps(data))   #Senden zum server

    client.loop_forever()
