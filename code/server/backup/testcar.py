import time
import paho.mqtt.client as mqtt
from random import *
import json
TOPIC = ""
BROKER_ADDRESS = "test.mosquitto.org"
PORT = 1883
name = ""
coor = ""
id = ""
subtopic = [
"hshl/mqtt_exercise/test/testcar/back",
"hshl/mqtt_exercise/get_position"
]
def dataVerification(msg):
    if len(json.loads(str(msg))) > 0 :
        return True
    else:
        return False
        pass
def send(object,topic):
    time.sleep(2)
    client = mqtt.Client("master")
    client.connect(BROKER_ADDRESS, PORT)
    name = object
    print("test")
    def __init__(self, name):
        self.name = name
    print("Send: " + topic)
    msg = str(name)
    print(msg)
    client.publish(topic, msg)
    client.loop()

def receive():
    temp = []
    client = mqtt.Client()
    client.connect(BROKER_ADDRESS, PORT)
    def on_message(client, userdata, message):
        msg = str(message.payload.decode("utf-8"))
        print("message received: ", msg)
        print("message topic: ", message.topic)
        temp =  [message.topic,msg]
        if dataVerification(msg) == True:
            messageprocessing(temp)
        else:
            print("Failure! Empty Message received")

    def on_connect(client, userdata, flags, rc):
        print("Server Connected to MQTT Broker: " + BROKER_ADDRESS)
        for i in range(0,len(subtopic)):
            print(str(subtopic[i]))
            client.subscribe(subtopic[i], 2)
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()
def messageprocessing(msg):
    global id
    global name
    global idCar
    data = ""
    js = json.loads(msg[1])
    if msg[0] == "hshl/mqtt_exercise/test/testcar/back" and str(name) == js['name']:
        id = str(js['id'])
        subtopic.append("hshl/mqtt_exercise/test/testcar/"+str(id)+"/call")
        receive()
    elif msg[0] == "hshl/mqtt_exercise/test/testcar/"+str(id)+"/call":
        pickUpCoordinates(js['coordinates'])
        data = {
        "id":id,
        "msg": "Arrival",
        "coordinates": js['coordinates']
        }
        send(json.dumps(data),"hshl/mqtt_exercise/test/testcar/"+str(id)+"/call/back")
        subtopic.append("hshl/mqtt_exercise/test/testcar/"+str(id)+"/call/destination")
        receive()
    elif msg[0] == "hshl/mqtt_exercise/test/testcar/"+str(id)+"/call/destination":
        driveDestination(js['destination'],js['name'])
        data ={
        "id":id,
        "msg": "Arrival at destination",
        "coordinates": js['destination']
        }
        send(json.dumps(data),"hshl/mqtt_exercise/test/testcar/"+id+"/call/destination/back")
        receive()
    elif msg[0] == "hshl/mqtt_exercise/get_position" and str(js['id']) == str(id):
        data={
        "id":id,
        "name":name,
        "coordinates":coor
        }
        send(json.dumps(data),"hshl/mqtt_exercise/set_position")
def driveDestination(destinationcoor,guestname):
    print("New destination, drive "+guestname+" to: "+destinationcoor)
    coor = destinationcoor
    time.sleep(1)
    print("Arrival at: "+destinationcoor)
def rndCoordinates():
    x = randint(0,4)
    y = randint(1,4)
    return str(y)+";"+str(x)
def register():
    global coor
    global name
    coor = rndCoordinates()
    data={
    "id": "register",
    "name": name,
    "coordinates":coor
    }
    send(json.dumps(data), "hshl/mqtt_exercise/test/testcar")
def pickUpCoordinates(pickupcoor):
    print("New destination: "+pickupcoor)
    coor = pickupcoor
    time.sleep(1)
    print("Arrival at: "+pickupcoor)
name = input()
register()
receive()
