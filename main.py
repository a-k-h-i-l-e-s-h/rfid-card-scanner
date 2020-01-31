
import threading
import json
import time
import os
import socket
from os.path import join, dirname
from dotenv import load_dotenv
load_dotenv( join(dirname(__file__), '.env'))
# USB input device reader
# from evdev import InputDevice, categorize, ecodes
# Import SDK packages
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
# For certificate based connection
MQTTClient = AWSIoTMQTTClient("alec-card-scan")
rootca=os.path.abspath("aws_certificate/root-CA.crt")
privatekey=os.path.abspath("aws_certificate/private.pem.key")
certificate=os.path.abspath("aws_certificate/certificate.pem.crt")
ENDPOINT = 'a2nuyvcpnn25yt-ats.iot.eu-west-1.amazonaws.com'
PORT = 8883
SCANNER = os.getenv("SCANNER")
SCANNER_TYPE = os.getenv("SCANNER_TYPE")
MQTTTOPIC = 'com.test/cardscan/' + SCANNER

cardScanQueue = []
status_connected = False
def is_connected():
    global status_connected
    global MQTTClient
    try:
        # connect to the host -- tells us if the host is actually
        # reachable
        socket.create_connection((ENDPOINT, PORT))
        MQTTClient.configureEndpoint(ENDPOINT, PORT)
        MQTTClient.configureCredentials(rootca, privatekey, certificate)
        MQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        MQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
        MQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
        MQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
        MQTTClient.connect()
        print('AWS IOT Connected')
        status_connected = True
    except OSError:
        print('AWS IOT Unreachable')
        status_connected = False
        time.sleep(5)   
        is_connected()
        

def cardScan():
    global cardScanQueue
    #device = InputDevice("/dev/input/event0") # my keyboard
    #for event in device.read_loop():
    #    if event.type == ecodes.EV_KEY:
    #        card_number = event.code
    #        cur_time =  str(int(round(time.time() * 1000)))
    #        scanner_type = confPar["DEFAULT","SCANNER_TYPE"]
    #        payload = '{"card_number":"'+card_number+'","scan_time":"'+cur_time+'","scanner_type":"'+scanner_type+'"}' 
    #        cardScanQueue.append(payload)


def publishtoMQTT():
    global cardScanQueue
    global MQTTClient
    while(True):
        print('cardScanQueue-length',len(cardScanQueue))
        if(len(cardScanQueue) > 0 and status_connected):
            payload = cardScanQueue.pop(0)
            MQTTClient.publish(MQTTTOPIC, payload, 0)
        else:
            time.sleep(1)    

def main():
    process0 = threading.Thread(target=is_connected, args=())
    process1 = threading.Thread(target=cardScan, args=())
    process2 = threading.Thread(target=publishtoMQTT, args=())
    process0.start()
    process1.start()
    process2.start()

main()
