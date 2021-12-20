from multiprocessing import Process
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


def sendWS(command):
    SendGcode = {
        "jsonrpc": "2.0",
        "method": "printer.gcode.script",
        "params": {
            "script": command
        },
        "id": 7466}
    print("Websocket" + command)
    ws.send(json.dumps(SendGcode))


def sendS(command):
    display.write("Nix da".encode('utf-8'))


def receiveWS():
    data = json.loads(ws.recv())
    if hasattr(data, "method") == True:
        if data["method"] == "notify_gcode_response":
            return data["params"]


def receiveS():
    data = display.readline().rstrip().decode("utf-8")
    return data


def rec():
    while True:
        x = receiveS()
        sendWS(x)


def sen():
    while True:
        y = receiveWS()
        sendS(y)


Process(target=rec).start()
Process(target=sen).start()
