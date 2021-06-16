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
destination = ""
name = "Peter"
subtopic = [
"hshl/mqtt_exercise/user/back"
]

###############################################################################

#Log In Data From Server
def getid():
    data = {
     "id": "register",
     "name": "Peter",
     "coordinates": coordinates
     }
    send(json.dumps(data),"hshl/mqtt_exercise/user")

###############################################################################

#Feedback loop From Server
def send(object,topic):
    time.sleep(2)
    client = mqtt.Client("client")
    client.connect(BROKER_ADDRESS, PORT)
    name = object
    print("User")
    def __init__(self, name):
        self.name = name
    print("Data Send To Server Addr: " + BROKER_ADDRESS)
    msg = str(name)
    print("Transmitted Informations: "+msg)
    client.publish(topic, msg)
    client.loop()

def receive():
    global id
    temp = []
    client = mqtt.Client("user")
    client.connect(BROKER_ADDRESS, PORT)
    def on_message(client, userdata, message):
        msg = str(message.payload.decode("utf-8"))
        print("Received Informations: ", msg)
        print("message topic: ", message.topic)
        print(msg)
        temp =  [message.topic,msg]
        processing(temp)

    Abfrage = 4


    def on_connect(client, userdata, flags, rc):
        print("Data Received by Server Addr: " + BROKER_ADDRESS)
        for i in range(0,len(subtopic)):
            print(str(subtopic[i]))
            client.subscribe(subtopic[i], 2)

    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_start()
    time.sleep(5)
    client.loop_stop()

# Random Coordniate Output
zahly = randint(1, 4)
zahlx = randint(0, 4)
coordinates = str(zahly)+";"+str(zahlx)

###############################################################################

#Call For Testcar
def ordertestcar():
    global id
    global cartype
    data1 = {
        "type": "testcar",
        "id": id,
        "coordinates": coordinates
        }
    cartype = "testcar"
    time.sleep(5)
    send(json.dumps(data1),"hshl/mqtt_exercise/user/"+str(id))


#Call For Taxi
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


#Call For police
def orderpolice():
    global id
    global cartype
    data2 = {
        "type": "police",
        "id": id,
        "coordinates": coordinates
        }
    cartype = "police"
    time.sleep(5)
    send(json.dumps(data2),"hshl/mqtt_exercise/user/"+str(id))


#Call For Ambulance
def orderambulance():
    global id
    global cartype
    data2 = {
        "type": "ambulance",
        "id": id,
        "coordinates": coordinates
        }
    cartype = "ambulance"
    time.sleep(5)
    send(json.dumps(data2),"hshl/mqtt_exercise/user/"+str(id))


#Call for Firefighter
def orderfire():
    global id
    global cartype
    data2 = {
        "type": "firefighter",
        "id": id,
        "coordinates": coordinates
        }
    cartype = "firefighter"
    time.sleep(5)
    send(json.dumps(data2),"hshl/mqtt_exercise/user/"+str(id))

###############################################################################

#Seting Vehicle Status To Free
def setToFree():
    global id
    global idCar
    global cartype
    print("SERVICE VEHICLE SET TO FREE")
    data = {
    "type": cartype,
    "id": id,
    "idCar": idCar,
    }
    send(json.dumps(data),"hshl/mqtt_exercise/user/"+str(id)+"/status/reset")

###############################################################################

#Processing Received Data
def processing(msg):
    global id
    global idCar
    global count
    global destination
    global name
    data = ""

    if cartype == "taxi":
        topictype = str("taxi/")
    elif cartype == "police":
        topictype = str("services/")
    elif cartype == "ambulance":
        topictype = str("services/")
    elif cartype == "firefighter":
        topictype = str("services/")
    elif cartype == "testcar":
        topictype = str("test/testcar/")

#Processing Received ID
    js = json.loads(msg[1])
    if msg[0]=="hshl/mqtt_exercise/user/back" and js['name'] == str(name):
        id = js['id']
        print(id)
        subtopic.append("hshl/mqtt_exercise/user/"+str(id)+"/order/back")


#Feedback For Ordering Servie
    elif msg[0] == "hshl/mqtt_exercise/user/"+str(id)+"/order/back" and str(js['type']) == cartype:
        coordinates = str(2)+";"+str(4) # festlegen der koordinaten  zu denen das testcar fahren soll
        print("idCar"+str(js['id'])) # textausgabe
        idCar = js['id']# zugewiesene id speichern
        data = {
        "id": id,
        "name": name,
        "coordinates": coordinates,
        }
        send(json.dumps(data),"hshl/mqtt_exercise/"+topictype+str(idCar)+"/call") #senden meiner korrdinaten an das mir zugeteilete testcar
        subtopic.append("hshl/mqtt_exercise/"+topictype+str(idCar)+"/call/back") #hinzufügen des topics für das mir zugeteilte testcar
        receive() # warten auf antwort


#ServiceCar Feedack For Arrival At User And Arrival At Destination
    elif msg[0] == "hshl/mqtt_exercise/"+topictype+str(idCar)+"/call/back" and str(js['msg']) == "arrival": # antwort vom servicefahrzeug das angeschrieben wurde
        destination = ""
        destination = str(randint(1,4))+  ";"+  str(randint(0,4)) # zufalls coordinaten als ziel
        data = {
        "id": id,
        "name": name,
        "destination": destination
        }
        send(json.dumps(data),"hshl/mqtt_exercise/"+topictype+str(idCar)+"/call/destination") # dem servicefahrzeug mein ziel übergeben
        subtopic.append("hshl/mqtt_exercise/"+topictype+str(idCar)+"/call/destination/back") # hinzufügen des neuen topics
        receive() # warten auf antwort
    elif msg[0] == "hshl/mqtt_exercise/"+topictype+str(idCar)+"/call/destination/back" and str(js['msg']) == "arrival at destination": #rückmeldung über ankunft am ziel
        print("Arrival at Destination: "+ destination) #textausgabe
        setToFree() # staus des servicefahrzeuges beim server auf free setzen

###############################################################################

#Processing User Input
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
        orderpolice()
        receive()
    elif userinput == "orderfire":
        orderfire()
        receive()
    elif userinput == "orderambulance":
        orderambulance()
        receive()
    elif userinput == "ordertestcar":
        ordertestcar()
        receive()
    elif userinput == "getout":
        setToFree()

while 0==0:
    print("Enter Operation: ")
    userin(input())

###############################################################################
