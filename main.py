import websocket
import serial

ws = websocket.WebSocket()
ws.connect("ws://localhost/websocket")
#ws.send("Hello, Server")


#def sendWS():


def receiveWS():
    print(ws.recv())


#def sendS():


#def receiveS():


while True:
    receiveWS()
