import websocket
import serial
import json


serialPort = "/dev/ttyAMA0"
baudrate = "115200"
display = serial.Serial()
display.baudrate = baudrate
display.port = serialPort
display.open()

ws = websocket.WebSocket()
ws.connect("ws://localhost/websocket")

command = "G28 X"

SendGcode = {
    "jsonrpc": "2.0",
    "method": "printer.gcode.script",
    "params": {
        "script": command
    },
    "id": 7466}


def sendWS():
    ws.send(json.dumps(SendGcode))


def receiveWS():
    data = ws.recv()
    print(json.loads(data))


# def sendS():


def receiveS():
    data = display.readline().rstrip().decode("utf-8")
    command = data


while True:
    sendWS()
    receiveWS()
    receiveS()
