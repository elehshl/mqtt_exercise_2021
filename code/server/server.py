
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
subtopic = ["hshl/mqtt_exercise/user","hshl/mqtt_exercise/taxi","hshl/mqtt_exercise/police","hshl/mqtt_exercise/firefighter","hshl/mqtt_exercise/ambulance","hshl/mqtt_exercise/user/+/status/reset"]

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
    print("Send Connected to MQTT Broker: " + BROKER_ADDRESS)
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
        client.subscribe("hshl/mqtt_exercise/user/0",2)
        print("Server Connected to MQTT Broker: " + BROKER_ADDRESS)
        for i in range(0,len(subtopic)):
            print(str(subtopic[i]))
            client.subscribe(subtopic[i], 2)
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()

def findnextCar(gpsUser,car): # find closest car
    for k in range(int(gpsUser.split(";")[0]),5):
        for i in range((k-1)*1, k+1):
            print("i ist:"+str(i))
            for j in range((i-1)*-1, i+1):

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
#msg[0] ist das topic und msg[1] ist die eigentliche
def dataVerification(msg):
    if len(json.loads(str(msg))) > 0 :
        return True
    else:
        return False
        pass
def messageprocessing(msg):
    js = {}
    js = json.loads(str(msg[1]))
    data = []
    #registration taxi

    if msg[0] == "hshl/mqtt_exercise/taxi" and str(js["id"]) == "register": #Taxi
        data.append(1)
        data.append(js['name'])
        data.append(js['coordinates'])
        #data.append(msg[1].split(",")[0])
        #data.append(msg[1].split(",")[1])
        #data.append(msg[1].split(",")[2])
        print(str(data[2]))
        registrationCar(data,0)
        #registration user
    elif msg[0] == "hshl/mqtt_exercise/user" and str(js['id']) == "register":       #user
        data.append(findid(user))   #call find next id
        data.append(js['name']) #decode name from js and store
        data.append(js['coordinates']) #decode coordinates from js and store
        #data.append(msg[1].split(",")[0])
        #data.append(msg[1].split(",")[1])
        #data.append(msg[1].split(",")[2])
        registrationUser(data)  #call user registration
        subtopic.append("hshl/mqtt_exercise/user/"+ str(data[0]))   #add new exclusiv topic for the client/user
        userdata = {            #and send this to the user
        "id": data[0],
        "name": data[1],
        }
        time.sleep(2) #delay is needed ??
        send(json.dumps(userdata),"hshl/mqtt_exercise/user/back")
        receive()
        #wait for order
    elif msg[0] == "hshl/mqtt_exercise/user/"+ str(js['id']) :#and js['type'] == "taxi":
        car = []
        car.append(findnextCar(js['coordinates'],taxi)) #search for the closest taxi
        print("car"+str(car[0]))
        #set status of the taxi to busy
        for i in range(0,len(taxi)):
            temp1 = str(car[0][0])
            temp2 = str(taxi[i][0])
            print(temp1+"=="+temp2)
            if temp1 == temp2:
                taxi[i][3] = "busy"
        ################################
        #send the taxi to the user
                print("sending")
                data = {
                "type":"taxi",
                "id": taxi[i][0],
                "name": taxi[i][1],
                "coordinates": taxi[i][2],
                "status": taxi[i][3]
                }
                send(json.dumps(data),"hshl/mqtt_exercise/user/"+str(js['id'])+"/order/back")
                print("send")
    elif msg[0] == "hshl/mqtt_exercise/user//status/reset":
        #############################
        print("TESTTEST##################################################")
        #wait for service registration
    elif msg[0] == "hshl/mqtt_exercise/services/police" or msg[0] == "hshl/mqtt_exercise/services/firefighter" or msg[0] == "hshl/mqtt_exercise/services/ambulance":
        if msg[0] == "hshl/mqtt_exercise/police":
            data.append(js['id'])
            data.append(js['name'])
            data.append(js['coordinates'])
        #    data.append(msg[1].split(",")[0])
            #data.append(msg[1].split(",")[1])
            #data.append(msg[1].split(",")[2])
            registrationCar(data,1)
        elif msg[0] == "hshl/mqtt_exercise/firefighter":
            data.append(js['id'])
            data.append(js['name'])
            data.append(js['coordinates'])
            #data.append(msg[1].split(",")[0])
            #data.append(msg[1].split(",")[1])
            #data.append(msg[1].split(",")[2])
            registrationCar(data,2)
        elif msg[0] == "hshl/mqtt_exercise/ambulance":
            data.append(js['id'])
            data.append(js['name'])
            data.append(js['coordinates'])
            #data.append(msg[1].split(",")[0])
            #data.append(msg[1].split(",")[1])
            #data.append(msg[1].split(",")[2])
            registrationCar(data,3)
receive()
