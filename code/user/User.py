import paho.mqtt.client as mqtt
from random import *
import time
import json
TOPIC = "hshl/mqtt_exercise/services"
BROKER_ADDRESS = "test.mosquitto.org"
PORT = 1883
id = ""
idCar = ""
count = 0
cartype = ""
userinput = ""


def send(object,topic):
    client = mqtt.Client("client")
    client.connect(BROKER_ADDRESS, PORT)
    name = object
    print("User")
    def __init__(self, name):
        self.name = name
    print(" SEND Connected to MQTT Broker: " + BROKER_ADDRESS)
    msg = str(name)
    print(msg)
    client.publish(topic, msg)
    client.loop()

def receive():
    global id
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

    Abfrage = 4



    def on_connect(client, userdata, flags, rc):
        print("receive Connected to MQTT Broker: " + BROKER_ADDRESS)
        client.subscribe("hshl/mqtt_exercise/user/back",2)
        client.subscribe("hshl/mqtt_exercise/user/"+str(id)+"/order/back", 2)

    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_start()
    time.sleep(5)
    client.loop_stop()
# zufalls coordinaten
zahly = randint(1, 4)
zahlx = randint(0, 4)
coordinates = str(zahly)+";"+str(zahlx)
#######
#order taxi
def ordertaxi():
    global id
    global cartype
    data1 = {
        "type": "taxi",
        "id": id,
        "coordinates": coordinates
        }
    cartype = "taxi"
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
#########
def setToFree(): #seting the status to free
    global id
    global idCar
    global cartype
    print("freeee")
    data = {
    "type": cartype,
    "id": id,
    "idCar": idCar,
    }
    send(json.dumps(data),"hshl/mqtt_exercise/user/"+str(id)+"/status/reset")

#erst einmal testweise dinge mit den erhaltenen nachrichten machen
def processing(msg):
    global id
    global idCar
    global count
    data = ""
    Abfrage = 1
    #die erhaltene id verarbeiten
    js = json.loads(msg[1])
    if msg[0]=="hshl/mqtt_exercise/user/back" and js['name'] == "Peter":
        id = js['id']
        print(id)
    elif msg[0] == "hshl/mqtt_exercise/user/"+str(id)+"/order/back" and js['type'] == "taxi":
        coordinates1 = str(2)+";"+str(4)
        print("idCa"+str(js['id']))
        idCar = js['id']
        data = {
        "id": id,
        "name": "User",
        "coordinates1": coordinates1,
        "topic": "hshl/mqtt_exercise/user"
        }
        send(json.dumps(data),"hshl/mqtt_exercise/taxi/"+str(id)+"/back")

    if Abfrage == 5:        #service fahrzeuge
        coordinates2 = str(zahly)+";"+str(zahlx)
        data = {
        "id": "2",
        "name": "User",
        "coordinates2": coordinates2,
        "topic": "hshl/mqtt_exercise/user"
        }
        send(json.dumps(data),"hshl/mqtt_exercise/services")
    ###
    if count == 0:
        count= count + 1
def userin(userinput):
    if userinput =="reg":
        getid()
        receive()
        pass
    elif userinput == "ordertaxi":
        ordertaxi()
        receive()
    elif userinput == "orderpolice":
        print("not implemented yet")
    elif userinput == "orderfire":
        print("not implemented yet")
    elif userinput == "orderambulance":
        print("not implemented yet")
    elif userinput == "getout":
        setToFree()
        exit()

while 0==0:
    print("Enter Operation: ")
    userin(input())
