#!/usr/bin/python

import sys
import time
import Adafruit_DHT
import json
import httplib, urllib
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(22,GPIO.IN)
GPIO.setup(17,GPIO.OUT)

deviceId = "D9xzoYqI"
deviceKey = "ngPOcmH2wT9QYocm"
sw=1
def post_to_mcs(payload): 
	headers = {"Content-type": "application/json", "deviceKey": deviceKey} 
	not_connected = 1 
	while (not_connected):
		try:
			conn = httplib.HTTPConnection("api.mediatek.com:80")
			conn.connect() 
			not_connected = 0 
		except (httplib.HTTPException, socket.error) as ex: 
			print("Error: %s" % ex) 
			time.sleep(1)
 
	conn.request("POST", "/mcs/v2/devices/" + deviceId + "/datapoints", json.dumps(payload), headers) 
	response = conn.getresponse() 
	print( response.status, response.reason, json.dumps(payload), time.strftime("%c")) 
	data = response.read() 
	conn.close()

#sensor_args = { '11': Adafruit_DHT.DHT11,
#                '22': Adafruit_DHT.DHT22,
#                '2302': Adafruit_DHT.AM2302 }
#if len(sys.argv) == 3 and sys.argv[1] in sensor_args:
#    sensor = sensor_args[sys.argv[1]]
#    pin = sys.argv[2]
#else:
#    print('Usage: sudo ./Adafruit_DHT.py [11|22|2302] <GPIO pin number>')
#    print('Example: sudo ./Adafruit_DHT.py 2302 4 - Read from an AM2302 connected to GPIO pin #4')
#    sys.exit(1)

while 1:
#        sw=(sw+1)%2
#	humidity, temperature= Adafruit_DHT.read_retry(11,4)
	h0, t0= Adafruit_DHT.read_retry(11,4)
       	sw = GPIO.input(22)
       	if sw==1:	
	       	GPIO.output(17,0)
                sw1=0
                print('0=unpress')
	else:
		GPIO.output(17,1)
                sw1=1
	       	print('1=press')
#        sw =0
	if h0 is not None and t0 is not None:
		print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(t0,h0))
	#	payload = {"datapoints":[{"dataChnId":"Humidity","values":{"value":h0}},
	#	{"dataChnId":"Temperature","values":{"value":t0}},{"dataChnId":"SwitchStatus","values":{"value":sw}}]} 
                payload = {"datapoints":[{"dataChnId":"Humidity","values":{"value":h0}},{"dataChnId":"Temperature","values":{"value":t0}},{"dataChnId":"SwatchStatus","values":{"value":sw1}}]}	
	        post_to_mcs(payload)
	#	time.sleep(0.3)
	else:
		print('Failed to get reading. Try again!')
		sys.exit(1)
#		time.sleep(1)
