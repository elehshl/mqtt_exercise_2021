import paho.mqtt.client as mqtt
from random import *
import time
TOPIC = "hshl/mqtt_exercise/services"
BROKER_ADDRESS = "test.mosquitto.org"
PORT = 1883

def send(object,topic):
    client = mqtt.Client("client")
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
        print(msg)
        temp =  [message.topic,msg]
    def on_connect(client, userdata, flags, rc):

        print("Connected to MQTT Broker: " + BROKER_ADDRESS)
        client.subscribe("hshl/mqtt_exercise/user/1/back", 2)
        client.subscribe("hshl/mqtt_exercise/taxi",2)
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()
zahly = randint(0, 4)
zahlx = randint(0, 4)
coordinates = str(zahly)+";"+str(zahlx)
send("1,Peter,"+coordinates,"hshl/mqtt_exercise/user")
time.sleep(5)
send("taxi,"+coordinates,"hshl/mqtt_exercise/user/1")
receive()
