import network
import ujson
from machine import Pin
import esp
esp.osdebug(None)
import gc
gc.collect()

try:
  import usocket as socket
except:
  import socket

 
SSID = "MacPaw-Guest"
PASSWORD = ""

def log(msg):
    print(msg)
 
def connect_wifi():
    station = network.WLAN(network.STA_IF)

    station.active(True)
    station.connect(SSID, PASSWORD)

    while station.isconnected() == False:
    pass

    print('Connection successful')
    print(station.ifconfig())

    led = Pin(2, Pin.OUT)


def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        log('connecting to network...')
        sta_if.active(True)
        sta_if.connect(SSID, PASSWORD)
        while not sta_if.isconnected():
            pass
    log('network config:'+str( sta_if.ifconfig()))
 
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
html = """<!DOCTYPE html>
<html>
    <head> <title>ESP8266</title> </head>
    <body> 
        Hello from Python web on ESP8266
    </body>
</html>
"""

status = {
    "isOpen": "true"
}

headers = '''HTTP/1.1 200 OK
Content-Type: application/json


'''

response = headers + ujson.dumps(status)

# do_connect()
# connect_wifi()
# start_myserver()