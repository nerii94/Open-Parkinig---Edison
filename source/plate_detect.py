"""Detects plates from webcam."""
import cv2
from openalpr import Alpr
import sys
import os
import requests
import json
# import paho.mqtt.client as client

headers = {'content-type': 'application/json'}
url = "http://requestb.in/vd5wylvd"
alpr = Alpr("us", "/etc/openalpr/openalpr.conf",
            "/usr/share/openalpr/runtime_data")

if not alpr.is_loaded():
    print "Error loading OpenALPR"
    sys.exit(1)

alpr.set_top_n(1)
alpr.set_default_region("us")

cap = cv2.VideoCapture(0)

# mqttc = client.Client()
# mqttc.connect("localhost", 1883, 60)

probablePlates = {}
wasPlate = False
numEx = 5
count = 0

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    temp = "frame%d.jpg" % ret
    cv2.imwrite(temp, frame)

    results = alpr.recognize_file(temp)

    if not wasPlate:
        count = 0

    if count == numEx:
        items = probablePlates.items()
        mostProbable = items[0]
        for plate in items:
            if plate[1] > mostProbable[1]:
                mostProbable = plate[0]
                data = {"plate": mostProbable}
                data = json.dumps(data)

                r = requests.post(url, params=data, headers=headers)
                # mqttc.publish("plates", payload=data, qos=0, retain=True)
                print r.status_code

        print mostProbable
        count += 1
        probablePlates = {}

    elif count < numEx:
        i = 0
        count += 1
        for plate in results['results']:
            i += 1
            print("Test #%d" % count)
            print("   %12s %12s" % ("Plate", "Confidence"))
            for candidate in plate['candidates']:
                prefix = "-"
                if candidate['matches_template']:
                    prefix = "*"
                info = "  %s %12s%12f" % (prefix, candidate['plate'],
                                          candidate['confidence'])
                print(info)

                if candidate['plate'] in probablePlates.keys():
                    probablePlates[candidate['plate']] += candidate['confidence']
                else:
                    probablePlates[candidate['plate']] = candidate['confidence']

            # mqttc.publish("plates", payload="end", qos=0, retain=True)

    wasPlate = bool(results['results'])

    cv2.imshow("Frame", gray)

    os.remove(temp)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
# Call when completely done to release memory
alpr.unload()
cv2.destroyAllWindows()
# mqttc.disconnect()
