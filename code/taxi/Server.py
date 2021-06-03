import paho.mqtt.client as mqtt
import json
from random import *

class car():

    cars = []


    def on_connect(client, userdata, flags, rc):             # Empfangen vom car
        print("Connected with result code "+str(rc))

        client.subscribe("hshl/mqtt_exercise/taxi", 2)

    def on_message(client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))
        if(msg.topic.endswith('car')):
          register_company(msg.payload)

        data = {

         "Fahrzeug": randint(1, 100),
         "GPS": "1234,1235"
         }

        client.publish("hshl/mqtt_exercise/server", json.dumps(data))


    def register_car(data):
        js = json.loads(data)
        car = car(js['name'], js['coordinaten '], js['topic'])
        cars.append(car)
        print('###############')
        for c in car:
            print(c.name)
            print(c.coordinaten )
            print('-------------')
        print('################')

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("test.mosquitto.org", 1883, 60)

    client.loop_forever()
