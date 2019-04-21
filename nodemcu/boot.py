
try:
  import usocket as socket
except:
  import socket

import network
import esp
import ujson
import gc
from machine import Pin

esp.osdebug(None)
gc.collect()


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
    headers = '''HTTP/1.1 200 OK
    Content-Type: application/json

    '''

    status = {
        "isOpen": "true"
    }

    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

    s = socket.socket()
    s.bind(addr)
    s.listen(5)

    print('listening on', addr)

    while True:
        cl, addr = s.accept()
        print('client connected from', addr)
        
        response = headers + ujson.dumps(status)
        cl.send(response)
        cl.close()

connect()
start_server()