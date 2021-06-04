import paho.mqtt.client as mqtt
from random import *
import time
import json
TOPIC = "hshl/mqtt_exercise/services"
BROKER_ADDRESS = "test.mosquitto.org"
PORT = 1883
id =""
def send(object,topic):
    client = mqtt.Client("client")
    client.connect(BROKER_ADDRESS, PORT)
    name = object
    print("test")
    def __init__(self, name):
        self.name = name
    print("Connected to MQTT Broker: " + BROKER_ADDRESS)
    msg = str(name)
    print(msg)
    client.publish(topic, msg)
    client.loop()

def receive():
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
        client.subscribe("hshl/mqtt_exercise/user/back",2)
        client.subscribe("hshl/mqtt_exercise/user/"+str(id)+"/back", 2)

    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()
# zufalls coordinaten
zahly = randint(0, 4)
zahlx = randint(0, 4)
coordinates = str(zahly)+";"+str(zahlx)
#######
#order taxi
def ordertaxi(id):
    data1 = {
        "type": "taxi",
        "id": id,
        "coordinates": coordinates
        }
    time.sleep(5)
    send(json.dumps(data1),"hshl/mqtt_exercise/user/"+str(id))
    ###########

     #id vom server bekommen
def getid():
    data = {
     "id": "register",
     "name": "Peter",
     "coordinates": coordinates
     }
    send(json.dumps(data),"hshl/mqtt_exercise/user")
    receive()
#########

#erst einmal testweise dinge mit den erhaltenen nachrichten machen
def processing(msg):
    print(msg[1])
    #die erhaltene id verarbeiten
    js = json.loads(msg[1])
    if msg[0]=="hshl/mqtt_exercise/user/back" and js['name'] == "Peter":
        id = js['id']
        print(id)
        pass
    ###
    ordertaxi(id)   #testweise ein taxi bestellen
getid()
time.sleep(2)
receive()
