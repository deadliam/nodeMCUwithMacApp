
import network
import ujson
# from machine import Pin
# esp.osdebug(None)

try:
  import usocket as socket
except:
  import socket

import gc
gc.collect()

ssid = 'MacPaw-Guest'
password = ''

def connect_wifi():
    response = ujson.dumps(status)

    station = network.WLAN(network.STA_IF)

    station.active(True)
    station.connect(ssid, password)

    while station.isconnected() == False:
      pass

    print('Connection successful')
    print(station.ifconfig())

    # led = Pin(2, Pin.OUT)

def start_myserver():
    log('start server method')
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    log('listening on'+str( addr))
    while True:
        cl, addr = s.accept()
        log('client connected from'+str(addr))
        cl.send(response)
        cl.close()
 
#main part

status = {
    "isOpen": "true"
}

headers = '''HTTP/1.1 200 OK
Content-Type: application/json


'''

response = ujson.dumps(status)

connect_wifi()
start_myserver()