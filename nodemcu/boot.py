
try:
  import usocket as socket
except:
  import socket

import network
import esp
import ujson
import gc
import utime
from machine import Pin
from time import sleep
from hcsr04 import HCSR04

sensor = HCSR04(trigger_pin=5, echo_pin=4)
esp.osdebug(None)
gc.collect()

isOpenValue = "false"

status = {
    "isOpen": isOpenValue
}   

def connect():
    ssid = 'Xiaomi_236D'
    password = 'ellisfromlos'

    station = network.WLAN(network.STA_IF)

    station.active(True)
    station.connect(ssid, password)

    while station.isconnected() == False:
      pass

    print('Connection successful')
    print(station.ifconfig())

    led = Pin(2, Pin.OUT)


def start_server():
    # headers = '''HTTP/1.1 200 OK
    # Content-Type: application/json

    # '''

    headers = '''HTTP/1.1 200 OK

    '''


    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

    s = socket.socket()
    s.bind(addr)
    s.listen(5)

    print('listening on', addr)

    distance = 0
    x = 0
    while True:
        cl, addr = s.accept()
        print('client connected from', addr)
        
        if x % 5 == 0:
            distance = sensor.distance_cm()
            x = 0

        if distance < 50:
            isOpenValue = "false"
        else:
            isOpenValue = "true"

        status = {
            "isOpen": isOpenValue
        }

        response = headers + ujson.dumps(status)
        cl.send(response)
        cl.close()
        x += 1


# Main

connect()
start_server()

