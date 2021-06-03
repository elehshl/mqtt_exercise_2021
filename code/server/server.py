
import time
import paho.mqtt.client as mqtt
import random
TOPIC = "hshl/mqtt_exercise/services"
BROKER_ADDRESS = "test.mosquitto.org"
PORT = 1883

taxi = [["1","Taxi4","0.4"],["2","Taxi5","1.-4"]]
police = []
firefighter = []
ambulance = []
user =[]
gpsUser = "0,1"
def registration(data,type):
    car = list(range(3,2))
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
            taxi.append(data)
        elif type == 1:
             police.append(data)
        elif type == 2:
            firefighter.append(data)
        elif type == 3:
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
        print(msg.split(",")[0])
        temp =  [message.topic,msg]
        messageprocessing(temp)
    def on_connect(client, userdata, flags, rc):

        print("Connected to MQTT Broker: " + BROKER_ADDRESS)
        client.subscribe("hshl/mqtt_exercise/services\police", 2)
        client.subscribe("hshl/mqtt_exercise/taxi",2)
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()

def findnextCar(gpsUser,car):
        for i in range(int(gpsUser.split(".")[0]), 4):
            print("i ist:"+str(i))
            for j in range((i-1), i+1):

                print("j ist:"+str(j))
                for c in range(0,len(car)):
                    print("search for car: "+ str(car[c]))
                    if car[c][2] == gpsUser:
                        print("same")
                        return car[c]
                    elif int(car[c][2].split(".")[0]) == -i and int(car[c][2].split(".")[1]) == j:
                        print("1 Das nächst gelegene fahrzeug ist:"+str(-i)+"."+str(j))
                        return car[c]
                    elif int(car[c][2].split('.')[0]) == i and int(car[c][2].split('.')[0]) == j:
                        print("2 Das nächst gelegene fahrzeug ist:"+str(i)+"."+str(j))
                        return car[c]
                    elif int(car[c][2].split('.')[0]) == j and int(car[c][2].split('.')[0]) == -i:
                        print("3 Das nächst gelegene fahrzeug ist:"+str(j)+"."+str(-i))
                        return Car[c]
                    elif int(car[c][2].split('.')[0]) == j and int(car[c][2].split('.')[0]) == i:
                        print("4 Das nächst gelegene fahrzeug ist:"+str(j)+"."+str(i))
                        return car[c]

def messageprocessing(msg):
    data = []
    print(format(msg[1]))
    if msg[0] == "hshl/mqtt_exercise/taxi":
        data.append(msg[1].split(",")[0])
        data.append(msg[1].split(",")[1])
        data.append(msg[1].split(",")[2])
        print(data[2])
        registration(data,0)
        for i in range(0,len(taxi)):
            print(str(taxi[i]))
            pass
    findnextCar("0.0",taxi)
receive()
