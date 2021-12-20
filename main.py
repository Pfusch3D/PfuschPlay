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


def receiveWS():
    ws_data = ws.recv()
    data = json.loads(ws_data)
    if "method" in data:
        if data["method"] == "notify_gcode_response":
            return data["params"]


def sendS(command):
    display.write(bytes("Hello World!", 'utf-8'))
    print(command)

###################################################################


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


Process(target=sen).start()
Process(target=rec).start()
