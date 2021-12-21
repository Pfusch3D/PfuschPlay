import serial
import time

display = serial.Serial("/dev/ttyAMA0", 115200)

#display.open()

while True:
    display.write(b"A1V 200")
    time.sleep(1)
