#!/usr/bin/python
import asyncio
import configparser
import sys
import serial
import websocket

config = configparser.RawConfigParser()
config.read(str(sys.argv[1]))

displaytype = str(config["display"]["displaytype"])
serialport = str(config["display"]["serialport"])
baudrate = int(config["display"]["baudrate"])
websocketurl = str(config["display"]["websocketurl"])
display = serial.Serial()
moonraker = websocket.WebSocketApp(websocketurl, on_message=messageWebsocket)


def connectDisplay():
    display.baudrate = baudrate
    display.port = serialport
    display.open()

def connectWebsocket():
    moonraker.run_forever()

def readDisplay():
    data = display.readline().decode("utf-8").replace("\r", "").replace("\n", "")
    return data

def writeDisplay(data):
    display.write((data + "\n").encode())

def messageWebsocket(moonraker, message):
    print(message)

def main():
    writeDisplay("J01")

if __name__ == "__main__":
    connectDisplay()
    connectWebsocket()
    main()

