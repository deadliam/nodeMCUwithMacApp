
try:
  import usocket as socket
except:
  import socket

import network
import esp
import ujson
import gc
import utime
from machine import Pin, PWM
from time import sleep
from hcsr04 import HCSR04 
from rtttl import RTTTL
import songs

sensor = HCSR04(trigger_pin=5, echo_pin=4)
esp.osdebug(None)
gc.collect()

tone = PWM(Pin(14, Pin.OUT), freq=0, duty=0)

isOpenValue = "false"

status = {
    "isOpen": isOpenValue
}  

def play_tone(freq, msec):
    print('freq = {:6.1f} msec = {:6.1f}'.format(freq, msec))
    if freq > 0:
        tone.duty(10)
        tone.freq(int(freq))
    sleep(msec*0.001)  # Play for a number of msec
    tone.duty(0)            # Stop playing
    sleep(0.01)        # Delay 50 ms between notes

def play_melody():
    tune = RTTTL(songs.find('Indiana'))
    for freq, msec in tune.notes():
        play_tone(freq, msec)
    tone.deinit()

# def handle_post_status(client):
#     (method, url, version) = socket.readline().split(b" ")
#     if method == b"POST":
#         return "POST POST"


def handle(sock, distance):
    # (method, url, version) = sock.readline()
    # headers = '''HTTP/1.1 200 OK
    # Content-Type: application/json

    # '''
    headers = '''HTTP/1.1 200 OK

    '''
    if distance < 50:
        isOpenValue = "false"
    else:
        isOpenValue = "true"

    status = {
        "isOpen": isOpenValue
    }

    response = headers + ujson.dumps(status)
    sock.send(response)
    sock.close()

def connect_wifi():
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
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    
    s = socket.socket()
    s.bind(addr)
    s.listen(5)

    print('listening on', addr)

    distance = 0
    x = 0

    while True:
        try:
            sock, addr = s.accept()
            handle(sock, distance)
        except:
            sock.write("HTTP/1.1 500 Internal Server Error\r\n\r\n")
            sock.write("<h1>Internal Server Error</h1>")

    
        if x % 10 == 0:
            distance = sensor.distance_cm()            
            x = 0
        x += 1

# Main
# connect_wifi()
# start_server()
