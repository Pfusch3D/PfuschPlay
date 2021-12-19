import websocket
import serial
import json

ws = websocket.WebSocket()
ws.connect("ws://localhost/websocket")

jsonTests = {
    "jsonrpc": "2.0",
    "method": "printer.gcode.script",
    "params": {
        "script": "G28"
    },
    "id": 7466}

ws.send(jsonTests)


#def sendWS():


def receiveWS():
    print(ws.recv())
    print("===========================")


#def sendS():


#def receiveS():


while True:
    receiveWS()
