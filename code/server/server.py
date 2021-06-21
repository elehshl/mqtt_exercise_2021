#Requirement: NF-S03
import time
import paho.mqtt.client as mqtt
from random import *
import json
import threading

TOPIC = "hshl/mqtt_exercise/services"
BROKER_ADDRESS = "test.mosquitto.org"
PORT = 1883

taxi = []#[["1","TestTaxi","4;0","free"],["2","TestTaxi2","2;1","free"]]
police = []
firefighter = []
ambulance = []
testcar = []
user =[]
gpsUser = ""
subtopic = ["hshl/mqtt_exercise/user","hshl/mqtt_exercise/taxi","hshl/mqtt_exercise/services/police","hshl/mqtt_exercise/services/firefighter","hshl/mqtt_exercise/services/ambulance","hshl/mqtt_exercise/user/+/status/reset","hshl/mqtt_exercise/test/testcar"]
def findcarname(id,type):
    if type == "taxi":
        return taxi[findindex(id,type)][1]
    if type == "testcar":
        return testcar[findindex(id,type)][1]
    if type == "ambulance":
        return ambulance[findindex(id,type)][1]
    if type == "police":
        return police[findindex(id,type)][1]
    if type == "firefighter":
        return firefighter[findindex(id,type)][1]
def findindex(idCar,type):
    if type == "taxi":
        for i in range(0,len(taxi)):
            if taxi[i][0]==idCar:
                return i
    elif type == "police":
        for i in range(0,len(police)):
            if police[i][0]==idCar:
                return i
    elif type == "ambulance":
        for i in range(0,len(ambulance)):
            if ambulance[i][0]==idCar:
                return i
    elif type == "firefighter":
        for i in range(0,len(firefighter)):
            if firefighter[i][0]==idCar:
                return i
    elif type =="testcar":
        for i in range(0,len(testcar)):
            if testcar[i][0]==idCar:
                return i


def periodicPosition(): #Requirement: NF-S01
    while 0==0:
        print("#Prüfe Fahrzeugposition:")
        print("     #Firefighter: "+str(len(firefighter)))
        print("     #ambulance: "+str(len(ambulance)))
        print("     #taxi: "+str(len(taxi)))
        print("     #testcar: "+str(len(testcar)))
        print("     #police: "+str(len(police)))
        for i in range(0,len(firefighter)):
            requestPosition(firefighter[i][0],"firefighter",firefighter[i][1]);
            pass
        for i in range(0,len(ambulance)):
            requestPosition(ambulance[i][0],"ambulance",ambulance[i][1]);
            pass
        for i in range(0,len(taxi)):
            requestPosition(taxi[i][0],"taxi",taxi[i][1]);
            pass
        for i in range(0,len(testcar)):
            requestPosition(testcar[i][0],"testcar",testcar[i][1]);
            pass
        for i in range(0,len(police)):
            requestPosition(police[i][0],"police",police[i][1]);
            pass
        time.sleep(5) #Requirement: NF-S02
    t2.do_run = False

#registration for user
def registrationUser(data):
    inliste = False
    for i in range(0,len(user)):    #alredy exists Requirement: F-S04
        if str(data[0]) == str(user[i][0]):
            inliste = True
    if inliste == False:    # no ? add! Requirement: F-S05
        user.append(data)
    elif inliste == True:   #yes ? print(user exists alredy !)
        print("#user bereits vorhanden")
# same but seperated for each car type  Requirement: F-S01
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
    elif type == 99:
        car = testcar
    for i in range(0,len(car)):# Requirement: F-S07
        if str(data[1]) == str(car[i][1]):
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
        elif type == 99:
            data.append("free")
            testcar.append(data)
    elif inliste == True: #Requirements: F-S12
        print("#Car already registered")
#############################################

def send(object,topic):
    canpub = True
    time.sleep(2)
    try:
        client = mqtt.Client("master")
        client.connect(BROKER_ADDRESS, PORT)
    except Exception as e:
        print("Failure: "+ str(e)+"Message not send")
        canpub = False
    name = object
    def __init__(self, name):
        self.name = name
    msg = str(name)
    print("Send: " + msg+ " On: "+ topic)
    if canpub == True:
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
        for i in range(0,len(subtopic)):
            client.subscribe(subtopic[i], 2)
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()
# find closest car Requirements: F-S03
def findnextCar(gpsUser,car):
    cancle = 0
    for k in range(int(gpsUser.split(";")[0]),5):
        for i in range((k-1)*(-1), k+1):
            print("i ist:"+str(i))
            for j in range((i-1)*(-1), i+1):

                print("j ist:"+str(j))
                for c in range(0,len(car)):
                    print("search for car: "+ str(car[c]))
                    if car[c][2] == gpsUser:
                        if car[c][3]== "free":#Requirements: F-S11
                            return car[c]
                        else:
                            c=c-1
                            cancle = cancle + 1
                    elif int(car[c][2].split(";")[0]) == -i and int(car[c][2].split(";")[1]) == j:
                        if car[c][3]== "free":#Requirements: F-S11
                            return car[c]
                        else:
                            c=c-1
                            cancle = cancle+1
                    elif int(car[c][2].split(';')[0]) == j and int(car[c][2].split(';')[0]) == -i:
                        if car[c][3]== "free":#Requirements: F-S11
                            return car[c]
                        else:
                            c=c-1
                            cancle = cancle+1
                    elif int(car[c][2].split(';')[0]) == j and int(car[c][2].split(';')[0]) == i:
                        if car[c][3]== "free":#Requirements: F-S11
                            return car[c]
                        else:
                            c=c-1
                            cancle = cancle+1
                    elif int(car[c][2].split(';')[0]) == i and int(car[c][2].split(';')[0]) == j:
                        if car[c][3]== "free":#Requirements: F-S11
                            return car[c]
                        else:
                            c=c-1
                            cancle = cancle+1
                    if cancle == 3:
                        return None
                        pass
# find next id #
def findid(object):
    highid = 0
    for i in range(0,len(object)):
        print(str(object[i]))
        if highid < int(object[i][0]):
            highid = object[i][0]
            print("new ID is: "+ str(highid))
    return highid + 1
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
def requestPosition(idCar,type,name):
    for i in range(0,len(type)):
        pass
    data ={
    "id":idCar,
    "name": str(name)
    }
    send(json.dumps(data),"hshl/mqtt_exercise/get_position")
########################
def statusReset(idCar,type):
    if type == "taxi":
        taxi[findindex(idCar,type)][3] = "free"
    elif type == "police":
        police[findindex(idCar,type)][3] = "free"
    elif type == "ambulance":
        ambulance[findindex(idCar,type)][3] = "free"
    elif type == "firefighter":
        firefighter[findindex(idCar,type)][3] = "free"
    elif type =="testcar":
        testcar[findindex(idCar,type)][3] = "free"
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
    elif type == "testcar":
        testcar[idCar][2] = coordinates
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


#wait for order Requirement: F-S02
    elif msg[0] == "hshl/mqtt_exercise/user/"+ str(js['id']):
        t2.do_run = False
        car = []
        tempcar = []
        if str(js['type']) == "taxi":
            car.append(findnextCar(js['coordinates'],taxi)) #search for the closest taxi
            tempcar = taxi
        elif str(js['type']) == "police":
            car.append(findnextCar(js['coordinates'],police)) #search for the closest police
            tempcar = police
        elif str(js['type']) == "firefighter":
            car.append(findnextCar(js['coordinates'],firefighter)) #search for the closest firefighter
            tempcar = firefighter
        elif str(js['type']) == "ambulance":
            car.append(findnextCar(js['coordinates'],ambulance)) #search for the closest ambulance
            tempcar = ambulance
        elif str(js['type']) == "testcar":
            car.append(findnextCar(js['coordinates'],testcar))
            tempcar = testcar
    # find id in data
        temp1 = str(car[0][0])
        for i in range(0,len(tempcar)):
            temp2 = str(tempcar[i][0])
    #set status to busy Requirement: F-S08
            if temp1 == temp2:
                if str(js['type']) == "taxi":
                    taxi[i][3] = "busy"
                elif str(js['type']) == "police":
                    police[i][3] = "busy"
                elif str(js['type']) == "firefighter":
                    firefighter[i][3] = "busy"
                elif str(js['type']) == "ambulance":
                    ambulance[i][3] = "busy"
                elif str(js['type']) =="testcar":
                    testcar[i][3] = "busy"
    #send the car to the user
                print("# send ordered car")
                data = {
                "type":js['type'],
                "id": tempcar[i][0],
                "name": tempcar[i][1],
                "coordinates": tempcar[i][2],
                "status": tempcar[i][3]
                }
                #Requirement: F-S06
                send(json.dumps(data),"hshl/mqtt_exercise/user/"+str(js['id'])+"/order/back")
                print("# Ordered car sent")
########################################################################################################
    #Reset status of cars
    elif msg[0] == "hshl/mqtt_exercise/user/"+str(js["id"])+"/status/reset":
        statusReset(int(js["idCar"]),str(js["type"]))
        requestPosition(js["idCar"],js["type"],str(findcarname(js["idCar"],str(js['type']))))
        print("#Status Reset to Free by"+str(js['id']))
        t2.join()
#########################################################################################################
    #registration taxi Requirement: F-S10
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
        #wait for service registration Requirement:  F-S09 & F-S10
    elif msg[0] == "hshl/mqtt_exercise/services/police" or msg[0] == "hshl/mqtt_exercise/services/firefighter" or msg[0] == "hshl/mqtt_exercise/services/ambulance":
#register Police
        if msg[0] == "hshl/mqtt_exercise/services/police" and str(js["id"]) == "register": #checlk for message {"id":"register", "name": "[irgend_ein_name]","coordinates": "irgend_welche koordinaten"} on adress "hshl/mqtt_exercise/services/police"
            data.append(findid(police)) #find an free id for a police car
            data.append(js['name']) #save his name temporarily
            data.append(js['coordinates'])   #save his coordinates temporarily
            registrationCar(data,1)   #call method register with the temporarily data and identifier 1
            print("#Register Police:"+str(js['name'])+"by"+str(data[0]))#print name and id
            subtopic.append("hshl/mqtt_exercise/services/police/"+ str(data[0]))  # add new topic to monizoring
            userdata = {            # dataset with new data
            "id": data[0],
            "name": data[1],
            }
            time.sleep(2) #delay is needed ??
            send(json.dumps(userdata),"hshl/mqtt_exercise/services/police/back") #send new id with the name on adress "hshl/mqtt_exercise/services/police/back"
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
    elif msg[0] == "hshl/mqtt_exercise/test/testcar" and str(js['id']) == "register":
        tempid = findid(testcar)
        data.append(tempid)
        data.append(js['name'])
        data.append(js['coordinates'])
        registrationCar(data,99)
        print("#Register Test_Car:"+str(js['name'])+"by"+str(data[0]))
        subtopic.append("hshl/mqtt_exercise/test/testcar/"+ str(data[0]))
        userdata = {            #and send this to the taxi
        "id": data[0],
        "name": data[1],
        }
        time.sleep(2) #delay is needed ??
        send(json.dumps(userdata),"hshl/mqtt_exercise/test/testcar/back")
print("Start Server:")
t1 = threading.Thread(target=periodicPosition)
t2 = threading.Thread(target=receive)
t1.start()
t2.start()
