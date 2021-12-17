import serial


serialPort = ""
baudrate = ""


display = serial.Serial()
display.baudrate = Baudrate
display.port = serialPort
display.open

while True:
	readData()


def readData():
	data = display.readline()
	print (data)
	return true

	
