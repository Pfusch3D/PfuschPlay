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
	print(data)
	if data == "A21 X":
		return "G28 X"
	elif data == "A21 Y":
		return "G28 Y"
	elif data == "A21 Z":
		return "G28 Z"
	elif data == "A21 C":
		return "G28"
	else:
		return data

def writeData(input):
	jdata = {"commands": [input]}
	requests.post(moonrakerURL, json=jdata)

while True:
	r_data = readData()
	writeData(r_data)

	
