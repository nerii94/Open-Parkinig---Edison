import time
import pyupm_ttp223 as ttp223
import requests
import json

url = "http://requestb.in/rqa2unrq"
headers = {'content-type': 'application/json'}

touch = ttp223.TTP223(4)
touch1 = ttp223.TTP223(8)

was_pressed = False

while 1:
    if touch.isPressed():
        if not was_pressed:
		print "Send Info"
		was_pressed = True
		data = {"Id": "AI", "Espacio": 1, "Disponible": False}
		data = json.dumps(data)
                requests.post(url, params=data, headers=headers)
    elif not touch.isPressed():
	if was_pressed:
		print "Send Info"
	        was_pressed = False
        	data = {"Id":"AI","Espacio": 1,"Disponible":True}
                data = json.dumps(data)
               	requests.post(url, params=data, headers=headers)

		
    elif touch1.isPressed():
	print touch1.name(), 'presionado'
    time.sleep(1)

del touch
del tochh1
