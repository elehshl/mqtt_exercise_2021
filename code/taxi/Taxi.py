import paho.mqtt.client as mqtt
import time
import json
from random import *

SERVER_ADDRESS = "test.mosquitto.org"
TOPIC = ""
PORT = 1883
coor = ""
name = ""
id = ""

subtopic = ["hshl/mqtt_exercise/taxi/back","hshl/mqtt_exercise/get_position"]

def dataVerification(msg): #Prüfung der gesendeten Daten, ist die Datei empty = false
    if len(json.loads(str(msg))) > 0 :
        return True
    else:
        return False
        pass

def send(object,topic): #Senden & Registrieren
    time.sleep(2)
    client = mqtt.Client("client")
    client.connect(SERVER_ADDRESS, PORT)
    name = object
    print("TAXI")
    def __init__(self,name):
        self.name = name
        print(" SEND Connected to MQTT Broker: " + SERVER_ADDRESS)
    msg = str(name)
    print(msg)
    client.publish(topic, msg)
    client.loop()

def receive(): #Empfangen & Rückatwort
    temp = []
    client = mqtt.Client()
    client.connect(SERVER_ADDRESS, PORT)
    def on_message(client, userdata, message):
        msg = str(message.payload.decode("utf-8"))
        print("message received: ", msg)
        print("message topic: ", message.topic)
        temp =  [message.topic,msg]
        if dataVerification(msg) == True:
            messageprocessing(temp)
        else:
            print("Message = Leer!")

    def on_connect(client, userdata, flags, rc):
        print("Server Connected to MQTT Broker: " + SERVER_ADDRESS)
        for i in range(0,len(subtopic)): # Um mehrere Adressen (subtopics) zu registrieren           
            print(str(subtopic[i]))
            client.subscribe(subtopic[i], 2)
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()


def messageprocessing(msg): #Verarbeitung der eingehenden Narrichten
    global name
    global id
    data = ""

    if msg[0] == "hshl/mqtt_exercise/taxi/back/" and str(name) == js['name']:  # Empfangen der ID
        id = str(js['id']) # Speichern der erhaltenen ID in die Lokale(Global) ID
        subtopic.append("hshl/mqtt_exercise/taxi/"+str(id)+"/call")
        receive() #warte auf eine Nachricht
    elif msg[0] == "hshl/mqtt_exercise/taxi/"+str(id)+"/call":
        pickUpCoordinates(js['coordinates'])   
        data = {
        "id":id,
        "msg": "Arrival",
        "coordinates": js['coordinates']
        }
        send(json.dumps(data),"hshl/mqtt_exercise/taxi/"+str(id)+"/call/back")
        subtopic.append("hshl/mqtt_exercise/taxi/"+str(id)+"/call/destination")
        receive() #warten auf eine Antwort
    elif msg[0] == "hshl/mqtt_exercise/taxi/"+str(id)+"/call/destination":
        driveDestination(js['destination'],js['name'])
        data ={
        "id":id,
        "msg": "Arrival at destination",
        "coordinates": js['destination']
        }
        send(json.dumps(data),"hshl/mqtt_exercise/taxi/"+id+"/call/destination/back")
        receive()
    elif msg[0] == "hshl/mqtt_exercise/get_position" and str(js['id']) == str(id): 
        data={
        "id":id,
        "name":name,
        "coordinates":coor
        }
        send(json.dumps(data),"hshl/mqtt_exercise/set_position") #Senden der neuen Position

def driveDestination(destinationcoor,guestname):
    print("New destination, drive "+guestname+" to: "+destinationcoor)
    coor = destinationcoor
    time.sleep(1)
    print("Arrival at: "+destinationcoor)

def rndCoordinates(): #Berechnungen der Coordinaten
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
    send(json.dumps(data), "hshl/mqtt_exercise/taxi")  # Senden der brechneten Coordinaten

def pickUpCoordinates(pickupcoor):
    print("New destination: "+pickupcoor)
    coor = pickupcoor
    time.sleep(1)
    print("Arrival at: "+pickupcoor)
    
print("Reg. Name:")    
name = input() #Eingabe vom Name

register()
receive()
