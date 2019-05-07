import esp
from machine import Pin
esp.osdebug(None)

SSID = "Kitcast-2Ghz" # Xiaomi_236D
PASS = "NoOneKnowsThis" # ellisfromlos

import network 
# вариант 1, микроконтроллер подключается к WI FI и на ИП адресе вешает веб сервер
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
print(sta_if.scan())
sta_if.connect(SSID, PASS) # Connect to an AP 
sta_if.isconnected() # Check for successful connection

# print("NETWORK CONFIG: ", sta_if.ifconfig())

led = Pin(2, Pin.OUT)

import slimWebServ
# вариант 2, микроконтроллер как точка доступа 192.168.4.1
# ap = network.WLAN(network.AP_IF) 
# ap.active(True) 
# ap.config(essid='Xiaomi_236D')
# ap.config(authmode=3, password='ellisfromlos') 

#import webrepl
#webrepl.start()

#import machine
#machine.freq() # get the current frequency of the CPU
#machine.freq(160000000) # set the CPU frequency to 160 MHz