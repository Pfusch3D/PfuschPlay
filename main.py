import serial
import requests


serialPort = "/dev/ttyAMA0"
baudrate = "115200"
moonrakerURL = "http://localhost:7125/api/printer/command"

display = serial.Serial()
display.baudrate = baudrate
display.port = serialPort
display.open()

def readData():
	data = display.readline().rstrip().decode("utf-8")
	#print(data)
	return data

def writeData(input):
	jdata = {"commands": [input]}
	requests.post(moonrakerURL, json=jdata)

while True:
	r_data = readData()
	writeData(r_data)

	
