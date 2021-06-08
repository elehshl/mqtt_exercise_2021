
import time
import paho.mqtt.client as mqtt
from random import *
import json
TOPIC = "hshl/mqtt_exercise/services"
BROKER_ADDRESS = "test.mosquitto.org"
PORT = 1883

taxi = []#[["1","TestTaxi","4;0","free"],["2","TestTaxi2","2;1","free"]]
police = []
firefighter = []
ambulance = []
user =[]
gpsUser = ""
subtopic = ["hshl/mqtt_exercise/user","hshl/mqtt_exercise/taxi","hshl/mqtt_exercise/services/police","hshl/mqtt_exercise/services/firefighter","hshl/mqtt_exercise/services/ambulance","hshl/mqtt_exercise/user/+/status/reset"]

#registration for user
def registrationUser(data):
    inliste = False
    for i in range(0,len(user)):    #alredy exists ?
        if str(data[0]) == str(user[i][0]):
            inliste = True
    if inliste == False:    # no ? add!
        user.append(data)
    elif inliste == True:   #yes ? print(user exists alredy !)
        print("user bereits vorhanden")
# same but seperated for each car type
def registrationCar(data,type):
    car = []
    inliste = False
    if type == 0:
        car = taxi
    elif type == 1:
        car = police
    elif type == 2:
        car = firefighter
    elif type == 3:
         car = ambulance
    for i in range(0,len(car)):
        if str(data[0]) == str(car[i][0]):
            inliste = True
    if inliste == False:
        if type == 0:
            data.append("free")
            taxi.append(data)
        elif type == 1:
            data.append("free")
            police.append(data)
        elif type == 2:
            data.append("free")
            firefighter.append(data)
        elif type == 3:
            data.append("free")
            ambulance.append(data)
    elif inliste == True:
        print("fahrezug bereits hinzugefügt")
#############################################

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

def findnextCar(gpsUser,car): # find closest car
    for k in range(int(gpsUser.split(";")[0]),5):
        for i in range((k-1)*(-1), k+1):
            print("i ist:"+str(i))
            for j in range((i-1)*(-1), i+1):

                print("j ist:"+str(j))
                for c in range(0,len(car)):
                    print("search for car: "+ str(car[c]))
                    if car[c][2] == gpsUser:
                        print("same")
                        return car[c]
                    elif int(car[c][2].split(";")[0]) == -i and int(car[c][2].split(";")[1]) == j:
                        print("1 Das nächst gelegene fahrzeug ist:"+str(-i)+"."+str(j))
                        return car[c]
                    elif int(car[c][2].split(';')[0]) == j and int(car[c][2].split(';')[0]) == -i:
                        print("3 Das nächst gelegene fahrzeug ist:"+str(j)+"."+str(-i))
                        return car[c]
                    elif int(car[c][2].split(';')[0]) == j and int(car[c][2].split(';')[0]) == i:
                        print("4 Das nächst gelegene fahrzeug ist:"+str(j)+"."+str(i))
                        return car[c]
                    elif int(car[c][2].split(';')[0]) == i and int(car[c][2].split(';')[0]) == j:
                        print("2 Das nächst gelegene fahrzeug ist:"+str(i)+"."+str(j))
                        return car[c]
# find next id #
def findid(object):
    highid = 0
    for i in range(0,len(object)):
        if highid < int(object[i][0]):
            highid = object[i][0]
    return highid
#######
 #check for empty message
def dataVerification(msg):
    if len(json.loads(str(msg))) > 0 :
        return True
    else:
        return False
        pass
##############################

 #call for new position
def requestPosition(idCar,type):
    name =""
    for i in range(0,len(type)):
        pass
    data ={
    "id":idCar,
    "name": name
    }
    send(data,"hshl/mqtt_exercise/get_position")
########################
def statusReset(idCar,type):
    if type == "taxi":
        taxi[idCar][3] = "free"
    elif type == "police":
        police[idCar][3] = "free"
    elif type == "ambulance":
        ambulance[idCar][3] = "free"
    elif type == "firefighter":
        firefighter[idCar][3] = "free"

    #store received coordinates
def storePosition(idCar,type,coordinates):
    if type == "taxi":
        taxi[idCar][2] = coordinates
    elif type == "police":
        police[idCar][2] = coordinates
    elif type == "ambulance":
        ambulance[idCar][2] = coordinates
    elif type == "firefighter":
        firefighter[idCar][2] = coordinates
########################################




#msg[0] ist das topic und msg[1] ist die eigentliche Nachricht
def messageprocessing(msg):
    js = {}
    js = json.loads(str(msg[1]))
    data = []


#registration user
    if msg[0] == "hshl/mqtt_exercise/user" and str(js['id']) == "register":       #user
        data.append(findid(user))   #call find next id
        data.append(js['name']) #decode name from js and store
        data.append(js['coordinates']) #decode coordinates from js and store
        registrationUser(data)  #call user registration
        subtopic.append("hshl/mqtt_exercise/user/"+ str(data[0]))   #add new exclusiv topic for the client/user
        userdata = {            #and send this to the user
        "id": data[0],
        "name": data[1],
        }
        time.sleep(2) #delay is needed ??
        send(json.dumps(userdata),"hshl/mqtt_exercise/user/back")
        receive()
####################
#Set new position in data
    elif msg[0] == "hshl/mqtt_exercise/set_position":
        storePosition(js["id"],js["type"],js["coordinates"])
#####################


#wait for order
    elif msg[0] == "hshl/mqtt_exercise/user/"+ str(js['id']):
        car = []
        tempcar = []
        if str(js['type']) == "taxi":
            car.append(findnextCar(js['coordinates'],taxi)) #search for the closest taxi
            tempcar.append(taxi)
        elif str(js['type']) == "police":
            car.append(findnextCar(js['coordinates'],police)) #search for the closest police
            tempcar.append(police)
        elif str(js['type']) == "firefighter":
            car.append(findnextCar(js['coordinates'],firefighter)) #search for the closest firefighter
            tempcar.append(firefighter)
        elif str(js['type']) == "ambulance":
            car.append(findnextCar(js['coordinates'],ambulance)) #search for the closest ambulance
            tempcar.append(ambulance)
        print("car"+str(car[0]))
    # find id in data
        temp1 = str(car[0][0])
        for i in range(0,len(tempcar)):
            temp2 = str(tempcar[i][0])
            print(temp1+"=="+temp2)
    #set status to busy
            if temp1 == temp2:
                if str(js['type']) == "taxi":
                    taxi[i][3] = "busy"
                elif str(js['type']) == "police":
                    police[i][3] = "busy"
                elif str(js['type']) == "firefighter":
                    firefighter[i][3] = "busy"
                elif str(js['type']) == "ambulance":
                    ambulance[i][3] = "busy"
    #send the car to the user
                print("# send ordered car")
                data = {
                "type":"taxi",
                "id": tempcar[i][0],
                "name": tempcar[i][1],
                "coordinates": tempcar[i][2],
                "status": tempcar[i][3]
                }
                send(json.dumps(data),"hshl/mqtt_exercise/user/"+str(js['id'])+"/order/back")
                print("# Ordered car sent")
########################################################################################################
    #Reset status of cars
    elif msg[0] == "hshl/mqtt_exercise/user/"+str(js["id"])+"/status/reset":
        statusReset(js["idCar"],js["type"])
        print("#Status Reset to Free by"+str(js['id']))
#########################################################################################################
    #registration taxi
    elif msg[0] == "hshl/mqtt_exercise/taxi" and str(js["id"]) == "register": #Taxi
        data.append(findid(taxi))
        data.append(js['name'])
        data.append(js['coordinates'])
        #data.append(msg[1].split(",")[0])
        #data.append(msg[1].split(",")[1])
        #data.append(msg[1].split(",")[2])
        print("#Register Taxi:"+str(js['name'])+"by"+str(data[0]))
        registrationCar(data,0)
        subtopic.append("hshl/mqtt_exercise/taxi/"+ str(data[0]))
        userdata = {            #and send this to the taxi
        "id": data[0],
        "name": data[1],
        }
        time.sleep(2) #delay is needed ??
        send(json.dumps(userdata),"hshl/mqtt_exercise/taxi/back")
################################################################################################################
        #wait for service registration
    elif msg[0] == "hshl/mqtt_exercise/services/police" or msg[0] == "hshl/mqtt_exercise/services/firefighter" or msg[0] == "hshl/mqtt_exercise/services/ambulance":
#register Police
        if msg[0] == "hshl/mqtt_exercise/services/police" and str(js["id"]) == "register":
            data.append(findid(police))
            data.append(js['name'])
            data.append(js['coordinates'])
            registrationCar(data,1)
            print("#Register Police:"+str(js['name'])+"by"+str(data[0]))
            subtopic.append("hshl/mqtt_exercise/services/police/"+ str(data[0]))
            userdata = {            #and send this to the taxi
            "id": data[0],
            "name": data[1],
            }
            time.sleep(2) #delay is needed ??
            send(json.dumps(userdata),"hshl/mqtt_exercise/services/police/back")
#############################################################################################################
#register Firefighter
        elif msg[0] == "hshl/mqtt_exercise/services/firefighter" and str(js["id"]) == "register":
            data.append(findid(firefighter))
            data.append(js['name'])
            data.append(js['coordinates'])
            registrationCar(data,2)
            print("#Register Firefighter:"+str(js['name'])+"by"+str(data[0]))
            subtopic.append("hshl/mqtt_exercise/services/firefighter/"+ str(data[0]))
            userdata = {            #and send this to the taxi
            "id": data[0],
            "name": data[1],
            }
            time.sleep(2) #delay is needed ??
            send(json.dumps(userdata),"hshl/mqtt_exercise/services/firefighter/back")
############################################################################################################
# register Ambulance
        elif msg[0] == "hshl/mqtt_exercise/services/ambulance" and str(js["id"]) == "register":
            data.append(findid(ambulance))
            data.append(js['name'])
            data.append(js['coordinates'])
            registrationCar(data,3)
            print("#Register Firefighter:"+str(js['name'])+"by"+str(data[0]))
            subtopic.append("hshl/mqtt_exercise/services/ambulance/"+ str(data[0]))
            userdata = {            #and send this to the taxi
            "id": data[0],
            "name": data[1],
            }
            time.sleep(2) #delay is needed ??
            send(json.dumps(userdata),"hshl/mqtt_exercise/services/ambulance/back")
receive()
