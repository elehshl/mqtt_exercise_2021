
import time
import paho.mqtt.client as mqtt
from random import *
TOPIC = "hshl/mqtt_exercise/services"
BROKER_ADDRESS = "test.mosquitto.org"
PORT = 1883

taxi = []#[["1","TestTaxi","4;0","free"],["2","TestTaxi2","2;1","free"]]
police = []
firefighter = []
ambulance = []
user =[]
gpsUser = ""
subtopic = ["hshl/mqtt_exercise/user","hshl/mqtt_exercise/taxi","hshl/mqtt_exercise/police","hshl/mqtt_exercise/firefighter","hshl/mqtt_exercise/ambulance"]
def registrationUser(data):
    inliste = False
    for i in range(0,len(user)):
        if str(data[0]) == str(user[i][0]):
            inliste = True

    if inliste == False:
        user.append(data)
    elif inliste == True:
        print("user bereits vorhanden")
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
        print("fahrezug bereits hinzu gefügt")


def send(object,topic):
    client = mqtt.Client("master")
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
    client = mqtt.Client()
    client.connect(BROKER_ADDRESS, PORT)
    def on_message(client, userdata, message):
        msg = str(message.payload.decode("utf-8"))
        print("message received: ", msg)
        print("message topic: ", message.topic)
        print("message name",message.Client)
        print(msg.split(",")[0])
        temp =  [message.topic,msg]
        messageprocessing(temp)
    def on_connect(client, userdata, flags, rc):
        print("Server Connected to MQTT Broker: " + BROKER_ADDRESS)
        for i in range(0,len(subtopic)):
            print(str(subtopic[i]))
            client.subscribe(subtopic[i], 2)
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()

def findnextCar(gpsUser,car):
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

def messageprocessing(msg):
    data = []
    print(format(msg[1]))
    if msg[0] == "hshl/mqtt_exercise/taxi":         #Taxi
        data.append(msg[1].split(",")[0])
        data.append(msg[1].split(",")[1])
        data.append(msg[1].split(",")[2])
        print(data[2])
        registrationCar(data,0)
        for i in range(0,len(taxi)):
            print(str(taxi[i]))
            pass
    elif msg[0] == "hshl/mqtt_exercise/user":       #user
        data.append(msg[1].split(",")[0])
        data.append(msg[1].split(",")[1])
        data.append(msg[1].split(",")[2])
        registrationUser(data)
        subtopic.append("hshl/mqtt_exercise/user/"+data[0])
        receive()
        print("joojooo")
    elif msg[0] == "hshl/mqtt_exercise/user/1" and msg[1].split(',')[0] == "taxi":
        print("hallo")
        car = []
        car.append(findnextCar(msg[1].split(',')[1],taxi))
        print("car"+str(car[0]))
        for i in range(0,len(taxi)):
            temp1 = str(car[0][0])
            temp2 = str(taxi[i][0])
            print(temp1+"=="+temp2)
            if temp1 == temp2:
                taxi[i][3] = "busy"
                print("sending")
                send(taxi[i],"hshl/mqtt_exercise/user/1/back")
                print("send")
    elif msg[0] == "hshl/mqtt_exercise/services/police" or msg[0] == "hshl/mqtt_exercise/services/firefighter" or msg[0] == "hshl/mqtt_exercise/services/ambulance":
        if msg[0] == "hshl/mqtt_exercise/police":
            data.append(msg[1].split(",")[0])
            data.append(msg[1].split(",")[1])
            data.append(msg[1].split(",")[2])
            registrationCar(data,1)
        elif msg[0] == "hshl/mqtt_exercise/firefighter":
            data.append(msg[1].split(",")[0])
            data.append(msg[1].split(",")[1])
            data.append(msg[1].split(",")[2])
            registrationCar(data,2)
        elif msg[0] == "hshl/mqtt_exercise/ambulance":
            data.append(msg[1].split(",")[0])
            data.append(msg[1].split(",")[1])
            data.append(msg[1].split(",")[2])
            registrationCar(data,3)
receive()
