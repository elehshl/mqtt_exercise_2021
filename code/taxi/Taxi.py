import paho.mqtt.client as mqtt
import json
from random import *

class car():

    def  __init__(self, name, coordinaten,zahl,taxi):
         self.name  = name
         self.coordinaten = coordinaten
         self.zahl = zahl
         self.taxi = taxi
        
    cars = []

    def on_connect(client, userdata, flags, rc):

        client.subscribe("hshl/mqtt_exercise/taxi", 2)

        client.subscribe("hshl/mqtt_exercise/server", 2)
        
        client.subscribe("hshl/mqtt_exercise/taxi/get_postion", 2)
        
        client.subscribe("hshl/mqtt_exercise/taxi/"+str(id)+"/back", 2)

    def on_message(client, userdata, msg):
        print(str(msg.payload))

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("test.mosquitto.org", 1883, 60)

    taxi = intput()
    
    zahly = randint(1, 4)
    zahlx = randint(0, 4)
    coordinates = str(zahly)+";"+str(zahlx)
    data = {
     "id": "register",
     "name": taxi,
     "coordinates": coordinates,
     "topic": "hshl/mqtt_exercise/taxi"
     }
    client.publish("hshl/mqtt_exercise/taxi",json.dumps(data))   #Senden zum server
    
    
     if msg[0] == "hshl/mqtt_exercise/taxi/get_postion":
            
     coordinates1 = cordinates1 + randint(1, 4)
     data = {
         "id" : 5
         "type" : taxi
      "postion": coordinates1, #Coordiante vom Zielort
     
     }
     client.publish("hshl/mqtt_exercise/server/set_postion,json.dumps(data)
    

    client.loop_forever()
