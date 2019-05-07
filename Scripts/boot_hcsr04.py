# import machine
import ujson
import socket
# from hcsr04 import HCSR04

# import uos
# import gc
# gc.collect()
# This file is executed on every boot (including wake-boot from deepsleep)
# import esp
# esp.osdebug(None)
# uos.dupterm(None, 1) # disable REPL on UART(0)
# import webrepl
# webrepl.start()

# pins = [machine.Pin(i, machine.Pin.IN) for i in (0, 2, 4, 5, 12, 13, 14, 15)]

# trigger_pin = 1
# echo_pin = 2

# sensor = HCSR04(trigger_pin=trigger_pin, echo_pin=echo_pin)

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

# html = """HTTP/1.1 200 OK
#
# <!DOCTYPE html>
# <html>
#     <head> <title>ESP8266 Pins</title> </head>
#     <body> <h1>ESP8266 Pins</h1>
#         <table border="1"> <tr><th>Pin</th><th>Value</th></tr> %s </table>
#     </body>
# </html>
# """

status = {
    "isOpen": "true"
}

headers = '''HTTP/1.1 200 OK
Content-Type: application/json


'''

print('listening on', addr)

while True:
    cl, addr = s.accept()
    print('client connected from', addr)
    cl_file = cl.makefile('rwb', 0)

    value = "Test123"

    status = {
        "isOpen": value
    }

    response = headers + ujson.dumps(status)

    cl.send(response)
    cl.close()