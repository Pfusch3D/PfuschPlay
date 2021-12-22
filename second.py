import serial
import time

display = serial.Serial()
display.port = "/dev/ttyAMA0"
display.baudrate = 115200
display.open()


# display.open()

time.sleep(2)
while True:
    display.write(b"A1V 200 \r\n")
    time.sleep(1)
