#!/usr/bin/python
import asyncio
import configparser
import sys
import serial

config = configparser.RawConfigParser()
config.read(str(sys.argv[1]))

displaytype = str(config['display']['displaytype'])
serialport = str(config['display']['serialport'])
baudrate = int(config['display']['baudrate'])
websocketurl = str(config['display']['websocketurl'])

def connect():
    display = serial.Serial(port=serialport, baudrate=baudrate, )  

def main():
    print("Display Typ: ", displaytype)
    print("Serial Port: ", serialport)
    print("Baudrate: ", baudrate) 
    print("websocket URL: ", websocketurl)

if __name__ == "__main__":
    main()