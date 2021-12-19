import websocket
import serial
import json

ws = websocket.WebSocket()
ws.connect("ws://localhost/websocket")

SendGcode = {
    "jsonrpc": "2.0",
    "method": "printer.gcode.script",
    "params": {
        "script": command
    },
    "id": 7466}

command = ""


def sendWS():
    ws.send(json.dumps(SendGcode))


def receiveWS():
    data = ws.recv()
    print(json.load(data))


# def sendS():


def receiveS():
    data = display.readline().rstrip().decode("utf-8")
    self.command = data


while True:
    receiveWS()
