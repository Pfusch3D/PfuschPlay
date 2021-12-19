import websocket
import serial
import json
import asyncio


ws = websocket.WebSocket()
ws.connect("ws://localhost/websocket")

command = ""

SendGcode = {
    "jsonrpc": "2.0",
    "method": "printer.gcode.script",
    "params": {
        "script": command
    },
    "id": 7466}


async def sendWS():
    while True:
        ws.send(json.dumps(SendGcode))


async def receiveWS():
    while True:
        data = ws.recv()
        print(json.loads(data))


# def sendS():


async def receiveS():
    while True:
        data = display.readline().rstrip().decode("utf-8")
        self.command = data


def run():
    sendWS()
    receiveWS()
    receiveS()


asyncio.run(run())
