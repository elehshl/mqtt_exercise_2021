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
] # da die topics spezifisch zur id passen müssen geht das ganze nur über dynamsiche aufnahme der neuen topics .... deswegen array
def dataVerification(msg): #prüfung der gesendeten daten ist die datei lweer = false
    if len(json.loads(str(msg))) > 0 :
        return True
    else:
        return False
        pass
def send(object,topic): #senden
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

def receive(): #empfangen
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
        for i in range(0,len(subtopic)):        # hier werden bei jedem lese befehl die neuen topics aufgenommen
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
    if msg[0] == "hshl/mqtt_exercise/test/testcar/back" and str(name) == js['name']:        # empfangen der id
        id = str(js['id']) # speichern der ehaltenen id in die lokale(aber global) id
        subtopic.append("hshl/mqtt_exercise/test/testcar/"+str(id)+"/call") #aufnehmen des neuen topics mit der spezifischen id in das array
        receive() #warte auf nachricht
    elif msg[0] == "hshl/mqtt_exercise/test/testcar/"+str(id)+"/call":                      #koordinaten den users
        pickUpCoordinates(js['coordinates'])    #aufruf der methode um zum uder zu fahren dafür werden die koordinaten benötigt
        data = {
        "id":id,
        "msg": "Arrival",
        "coordinates": js['coordinates']
        }
        send(json.dumps(data),"hshl/mqtt_exercise/test/testcar/"+str(id)+"/call/back") # senden der nachricht
        subtopic.append("hshl/mqtt_exercise/test/testcar/"+str(id)+"/call/destination") #aufnehmen des neuen topics in das topic array
        receive() #warten auf antwort
    elif msg[0] == "hshl/mqtt_exercise/test/testcar/"+str(id)+"/call/destination":      #zielkoordinaten
        driveDestination(js['destination'],js['name']) #fahren zum wunschzuiel des kunden benötigt werden die korrdinaten und name
        data ={
        "id":id,
        "msg": "Arrival at destination",
        "coordinates": js['destination']
        }
        send(json.dumps(data),"hshl/mqtt_exercise/test/testcar/"+id+"/call/destination/back") # senden der erreich nachricht für das ziel
        receive()#warten auf die nachricht des servers zum bekommen der position
    elif msg[0] == "hshl/mqtt_exercise/get_position" and str(js['id']) == str(id): #neue position für den server
        data={
        "id":id,
        "name":name,
        "coordinates":coor
        }
        send(json.dumps(data),"hshl/mqtt_exercise/set_position")
def driveDestination(destinationcoor,guestname):                        #die fahrt zum ziel des kunden
    print("New destination, drive "+guestname+" to: "+destinationcoor) #textausgabe
    coor = destinationcoor #setzen der zielkoordinaten in den standort des fahrzeugs
    time.sleep(1) #schlafen eine sekunde
    print("Arrival at: "+destinationcoor)
def rndCoordinates():   #random koordinaten  y;x
    x = randint(0,4)    # random koordinate von x
    y = randint(1,4)    # random koordinate von y
    return str(y)+";"+str(x)
def register():                 #regestrieren
    global coor
    global name
    coor = rndCoordinates() #
    data={
    "id": "register",
    "name": name,
    "coordinates":coor
    }
    send(json.dumps(data), "hshl/mqtt_exercise/test/testcar")
def pickUpCoordinates(pickupcoor):          #theoretisch würde hier das fahren zum user stehen
    print("New destination: "+pickupcoor) #textausgabe
    coor = pickupcoor   #setzen der pickup koorindanten zu dem standkoordinaten
    time.sleep(1)#warten
    print("Arrival at: "+pickupcoor) #textausgabe
name = input()
register()
receive()
