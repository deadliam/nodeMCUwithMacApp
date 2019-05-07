import machine
import ujson
# import uos
# import gc
# gc.collect()
# This file is executed on every boot (including wake-boot from deepsleep)
# import esp
# esp.osdebug(None)
# uos.dupterm(None, 1) # disable REPL on UART(0)
# import webrepl
# webrepl.start()

pins = [machine.Pin(i, machine.Pin.IN) for i in (0, 2, 4, 5, 12, 13, 14, 15)]


status = {
    "isOpen": "true"
}

headers = '''HTTP/1.1 200 OK
Content-Type: application/json


'''

response = headers + ujson.dumps(status)

import socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print('listening on', addr)

while True:
    cl, addr = s.accept()
    print('client connected from', addr)
    cl_file = cl.makefile('rwb', 0)

    cl.send(response)
    cl.close()