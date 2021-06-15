import paho.mqtt.client as mqtt
import json
from random import *
BROKER_ADDRESS = "test.mosquitto.org"
PORT = 1883
import time
id = ""
name = ""
coor = ""
subtopic = [
"hshl/mqtt_exercise/services/firefighter/back",
"hshl/mqtt_exercise/get_position"
]


def send(topic, object): #senden
    client = mqtt.Client("client")
    client.connect(BROKER_ADDRESS, PORT)
    name = object
    print("Police")
    def __init__(self, name):
            self.name = name
    print(" SEND Connected to MQTT Broker: " + BROKER_ADDRESS)
    msg = str(name)
    print(msg)
    client.publish(topic, msg)
    client.loop()

def receive(): #empfangen
    global id
    temp = []
    client = mqtt.Client("firefighter")
    client.connect(BROKER_ADDRESS, PORT)
    def on_message(client, userdata, message):
        msg = str(message.payload.decode("utf-8"))
        print("message received: ", msg)
        print("message topic: ", message.topic)
        print(msg)
        temp =  [message.topic,msg]
        processing(temp)


    def on_connect(client, userdata, flags, rc):
        print("Server Connected to MQTT Broker: " + BROKER_ADDRESS)
        for i in range(0,len(subtopic)):        # hier werden bei jedem lese befehl die neuen topics aufgenommen
            print(str(subtopic[i]))
            client.subscribe(subtopic[i], 2)

    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()

def processing(msg):
    global id
    global name
    js = json.loads(msg[1])
    if "hshl/mqtt_exercise/services/firefighter/back" == msg[0] and str(js['name']) == str(name):
        id = js['id']
        print(id)
    elif msg[0] == "hshl/mqtt_exercise/services/firefighter/"+str(id)+"/call":                      #koordinaten des users
        drivetoUser(js['coordinates'])    #aufruf der methode um zum user zu fahren dafür werden die koordinaten benötigt
        data = {
        "id":id,
        "msg": "Arrival",
        "coordinates": js['coordinates']
        }
        send(json.dumps(data),"hshl/mqtt_exercise/services/firefighter/"+str(id)+"/call/back") # senden der nachricht
        subtopic.append("hshl/mqtt_exercise/services/firefighter/"+str(id)+"/call/destination") #aufnehmen des neuen topics in das topic array
        receive() #warten auf antwort
    elif msg[0] == "hshl/mqtt_exercise/services/firefighter/"+str(id)+"/call/destination":      #zielkoordinaten
        userDestination(js['destination'],js['name']) #fahren zum wunschzuiel des kunden benötigt werden die korrdinaten und name
        data ={
        "id":id,
        "msg": "Arrival at destination",
        "coordinates": js['destination']
        }
        send(json.dumps(data),"hshl/mqtt_exercise/services/firefighter/"+id+"/call/destination/back") # senden der erreicht nachricht für das ziel
        receive()#warten auf die nachricht des servers zum bekommen der position
    elif msg[0] == "hshl/mqtt_exercise/get_position" and str(js['id']) == str(id): #neue position für den server
        data={
        "id":id,
        "name":name,
        "coordinates":coor
        }
        send(json.dumps(data),"hshl/mqtt_exercise/set_position")

def userDestination(destinationcoor, guestname):
    print("New destination, drive "+guestname+" to: "+destinationcoor) #textausgabe
    coor = destinationcoor #setzen der zielkoordinaten in den standort des fahrzeugs
    time.sleep(1) #schlafen eine sekunde
    print("Arrival at: "+destinationcoor)

def drivetoUser(usercoor):
    print("New destination: "+usercoor) #textausgabe
    coor = usercoor   #setzen der pickup koorindanten zu dem standkoordinaten
    time.sleep(1)#warten
    print("Arrival at: "+usercoor) #textausgabe

def firefightercoor():
    zahly = randint(0, 4)
    zahlx = randint(0, 4)
    return str(zahly)+";"+str(zahlx)


def registration():
    global coor
    global name
    coor = firefightercoor()

    data = {
    "id": "register",
    "name": name,
    "coordinates": coor
    }
    send("hshl/mqtt_exercise/services/firefighter", json.dumps(data))

print("Gib einen Namen ein:")
name = input()
registration()
receive()
