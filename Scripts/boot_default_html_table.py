import machine
import ujson
import socket
from hcsr04 import HCSR04

pins = [machine.Pin(i, machine.Pin.IN) for i in (0, 2, 4, 5, 12, 13, 14, 15)]

trig_pin = 4
echo_pin = 3

sensor = HCSR04(trig_pin, echo_pin)

html = """HTTP/1.1 200 OK

<!DOCTYPE html>
<html>
    <head> <title>ESP8266 Pins</title> </head>
    <body> <h1>ESP8266 Pins</h1>
        <table border="1"> <tr><th>Pin</th><th>Value</th></tr> %s </table>
    </body>
</html>
"""

headers = '''HTTP/1.1 200 OK
Content-Type: application/json


'''

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

print('listening on', addr)

SSID = "Xiaomi_236D"
PASSWORD = "ellisfromlos"

def connect_wifi():
    station = network.WLAN(network.STA_IF)

    station.active(True)
    station.connect(SSID, PASSWORD)

    while station.isconnected() == False:
        pass

    print('Connection successful')
    print(station.ifconfig())

    led = Pin(2, Pin.OUT)

connect_wifi()

while True:
    cl, addr = s.accept()
    print('client connected from', addr)

    if sensor.distance_cm < 10:
        status = {
           "isOpen": "false"
        }
    else:
        status = {
           "isOpen": "true"
        }

    response = headers + ujson.dumps(status)

    # cl_file = cl.makefile('rwb', 0)
    # while True:
    #     line = cl_file.readline()
    #     if not line or line == b'\r\n':
    #         break
    # rows = ['<tr><td>%s</td><td>%d</td></tr>' % (str(p), p.value()) for p in pins]
    # response = html % '\n'.join(rows)
    cl.send(response)
    cl.close()