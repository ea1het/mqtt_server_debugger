# -*- coding: utf-8 -*-
# pylint: disable=locally-disabled, multiple-statements
# pylint: disable=fixme, line-too-long, invalid-name
# pylint: disable=W0703

""" MQTT server debugger """

__author__ = 'EA1HET'
__date__ = '20/05/2020'


import paho.mqtt.client as mqtt
import ssl


def on_connect(mqttc, obj, flags, rc):
    # rc = 0 --> all good
    # rc = 5 --> not authenticated
    print("rc: " + str(rc))


def on_message(mqttc, obj, msg):
    print(msg.topic + " / " + str(msg.qos) + " / " + str(msg.payload.decode('utf-8')))


def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))


def on_subscribe(mqttc, obj, mid, granted_qos):
    print("subscribed: " + str(mid) + " / " + str(granted_qos))


def on_log(mqttc, obj, level, string):
    print(string.decode('utf-8'))


def main(transport, tls, username, password, host, port, timeout):
    mqttc = mqtt.Client(transport=transport)
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish
    mqttc.on_subscribe = on_subscribe

    mqttc.username_pw_set(username=username, password=password)

    if tls:
        mqttc.tls_set(None, None, None, ciphers=None,
                      cert_reqs=ssl.CERT_NONE, tls_version=ssl.PROTOCOL_TLSv1_2)
        mqttc.tls_insecure_set(True)

    mqttc.connect(host, port, timeout)
    mqttc.subscribe("#", 0)
    # If you want to debug the mqtt server (mosquitto), you can enable the next line
    # mqttc.subscribe("$SYS/#", 0)
    mqttc.loop_forever()


if __name__ == '__main__':
    main(
        # transport = 'websockets' or 'tcp'
        transport='tcp',
        username='admin',
        password='admin',
        host='localhost',
        # port = typically 1883 (tcp), 8883 (tcp over tls) or 9001 (websockets over tls)
        port=8883,
        # tls = true or false; works in combination to port and transport
        tls=True,
        timeout=60
    )
