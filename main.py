import random
import time

import serial.tools.list_ports
import paho.mqtt.client as paho
from paho import mqtt
from paho.mqtt import client as mqtt_client
from VoiceAssistant import VoiceAssistant
from multiprocessing import Queue

topic = "python/mqtt"

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc==0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code ", str(rc))
    client = mqtt_client.Client(f'subscribe-{random.randint(0, 100)}')
    client.username_pw_set("da871rad", "arduinoRisa1")
    client.on_connect = on_connect
    client.connect("45cbd8c3198849d29e0b41255669e45a.s2.eu.hivemq.cloud", 8883)
    return client

def publish(client, mesaj):

        msg = f"messages: {mesaj}"
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")


if __name__ == '__main__':
    print("Hi. I am ready")
    ports = serial.tools.list_ports.comports()
    serialInst = serial.Serial()

    portList = []
    for port in ports:
        portList.append(str(port))
        print(str(port))

    serialInst.baudrate = 9600
    serialInst.port = "COM6"
    serialInst.open()

    print("Let's go")
    queue = Queue()
    assistant = VoiceAssistant(queue)
    print(assistant.webScrapingWeather())

    # client = paho.Client(client_id="da871rad", userdata=None, protocol=paho.MQTTv5)
    # client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)

    client = connect_mqtt()


    while(True):
        if serialInst.in_waiting:
            line = serialInst.readline()
            output = line.decode('utf').rstrip("\n").rstrip("\r")
            #print(output)
            if(str(output) == "OPENED!"):
                line = serialInst.readline()
                temp = line.decode('utf').rstrip("\n").rstrip("\r")
                assistant.turn_on(temp)
                publish(client, "Clapped!")
            elif(str(output) == "Clapped!"):
                assistant.count()

                #assistant.queue.put("clap")












