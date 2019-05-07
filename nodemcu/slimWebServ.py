
import socket
import time
import utime
import ujson
import songs
import machine
# from hcsr04 import HCSR04 
from rtttl import RTTTL
from machine import Pin, PWM
from libSlimWebServ import *

# sensor = HCSR04(trigger_pin=5, echo_pin=4)
tone = PWM(Pin(14, Pin.OUT), freq=0, duty=0)
button = Pin(12, Pin.IN, Pin.PULL_UP)

isOpenValue = "false"

status = {
    "isOpen": isOpenValue
}  

def play_tone(freq, msec):
    # print('freq = {:6.1f} msec = {:6.1f}'.format(freq, msec))
    if freq > 0:
        tone.duty(10)
        tone.freq(int(freq))
    time.sleep(msec*0.001)  # Play for a number of msec
    tone.duty(0)            # Stop playing
    time.sleep(0.01)        # Delay 50 ms between notes

def play_melody(song='closed'):
    print("Play melody: ", song)
    tune = RTTTL(songs.find(song))
    for freq, msec in tune.notes():
        play_tone(freq, msec)
    tone.deinit()

#   Вешаем на текущий адрес машины на 80 порт, прослушку порта
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
#   Каталог - корень для веб сервера
patch = ""
 
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(addr)
serversocket.listen(0)

requests_count = 0
last_date = utime.time()

print('Server is waiting for connections.')
play_melody('closed')

while True:
    try:
        conn, addr = serversocket.accept()
        conn.settimeout(3)
        data = conn.recv(1024)    
    except:
        pass
    
    print('Connection:', addr)
    print('------------------------------')
    print("Request Data from Browser")
    print('------------------------------')
    # print(data)    
    
    data_split = data.split(b'\r\n')
    print(data_split)
    
    #   Проверяем то что запрос на сервер адекватный
    if (data == b'') or (data_split[-1] != b'' and data_split[-2] != b''):
        conn.close()
        continue
    #   Берем параметры с запроса клиента
    method = data_split[0].split(b' ')[0]
    link = str(data_split[0].split(b' ')[1])    
    
    if method == b'POST':
        # Reset Nodemcu by request: POST http://192.168.31.116/reset
        if "reset" in link:
            machine.reset()

        varHtmlDict = requestPost(link=link)
        try:
            song_name = varHtmlDict['song']
            play_melody(song_name)
        except:
            play_melody()
        
        print("============= POST ==============")

    if method == b'GET':

        headers = '''HTTP/1.1 200 OK

        '''

        # Condition for button state
        if not button.value():
            isOpenValue = "false"
            print("BUTTON VALUE: ", button.value())
        else:
            isOpenValue = "true"
            print("BUTTON VALUE: ", button.value())

        status = {
            "isOpen": isOpenValue
        }

        # if "vcc" in link:
        #     vcc = machine.ADC(0)
        #     volts = vcc.read() * 1.024
        #     status = {
        #         "isOpen": volts
        #     }  
        
        response = headers + ujson.dumps(status)
        conn.send(response)

    conn.close()
    time.sleep(0.1)
        
    print("UTIME: ", utime.time())
    print("isOpen Value: ", isOpenValue)

# Request Data from Browser
# ------------------------------
# [b'POST / HTTP/1.1', b'cache-control: no-cache', b'Postman-Token: 627cf5c3-c4b9-48d0-8baa-09948e9eda3a', 
# b'User-Agent: PostmanRuntime/7.6.1', b'Accept: */*', 
# b'Host: 192.168.31.116', b'accept-encoding: gzip, deflate', 
# b'content-length: 0', b'Connection: keep-alive', b'', b'']
# Connection: ('192.168.31.154', 63575
