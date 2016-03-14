import time
import pyupm_ttp223 as ttp223
import requests
import json

url = "http://requestb.in/rqa2unrq"
headers = {'content-type': 'application/json'}

touch1 = ttp223.TTP223(4)
touch1Pressed = False
touch2 = ttp223.TTP223(8)
touch2Pressed = False


def sendInfo(touch, tId, Pressed):
    if touch.isPressed():
        if not Pressed:
            print "Send Info"
            Pressed = True
            data = {"Id": "AI", "Espacio": tId, "Disponible": False}
            data = json.dumps(data)
            requests.post(url, params=data, headers=headers)
    elif not touch.isPressed():
        if Pressed:
            print "Send Info"
            Pressed = False
            data = {"Id": "AI", "Espacio": tId, "Disponible": True}
            data = json.dumps(data)
            requests.post(url, params=data, headers=headers)
    return Pressed
while True:
    touch1Pressed = sendInfo(touch1, 1, touch1Pressed)
    touch2Pressed = sendInfo(touch2, 2, touch2Pressed)
    print touch1Pressed

    time.sleep(1)

del touch1
del touch2
