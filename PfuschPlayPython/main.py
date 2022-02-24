#!/usr/bin/python
import configparser
import sys
import serial

config = configparser.RawConfigParser()
config.read(str(sys.argv[1]))

displaytype = config['display']['displaytype']
serialport = config['display']['serialport']
baudrate = config['display']['baudrate']
websocketurl = config['display']['websocketurl']

def connect:
    ser = serial.Serial(port=serialport)  


def main():
    print("Display Typ: ", displaytype)
    print("Serial Port: ", serialport)
    print("Baudrate: ", baudrate) 
    print("websocket URL: ", websocketurl)

if __name__ == "__main__":
    main()