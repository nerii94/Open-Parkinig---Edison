import paho.mqtt.client as mqtt
message = 'ON'

def doSomething(plate):
    print("is " + plate + " correct?")

def on_connect(mosq, obj, rc):
    mqttc.subscribe("plates", 0)
    print("rc: " + str(rc))

def on_message(mosq, obj, msg):
    global message
    # print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    message = msg.payload
    if "|" in message:
        plate = message.split("|")
        plate[1].strip(' \t\n\r')
        p = plate[0].strip(' \t\n\r')
        doSomething(p)

    mqttc.publish("f2", msg.payload)

def on_publish(mosq, obj, mid):
    pass

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(mosq, obj, level, string):
    print(string)

mqttc = mqtt.Client()
# Assign event callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
# Connect
mqttc.connect("localhost", 1883, 60)
# Continue the network loop
mqttc.loop_forever()
