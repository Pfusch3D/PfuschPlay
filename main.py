from multiprocessing import Process
import websocket
import serial
import json
import config
import time

display = serial.Serial()
display.baudrate = config.PfuschPlay["baudrate"]
display.port = config.PfuschPlay["serialPort"]
display.open()

ws = websocket.WebSocket()
ws.connect(config.PfuschPlay["websocketURL"])


def receiveWS():
    ws_data = ws.recv()
    data = json.loads(ws_data)
    if "method" in data:
        if data["method"] == "notify_gcode_response":
            return data["params"]


def sendS(commandone):
    if commandone:
        datazero = str(commandone)
        dataone = datazero.replace("[", "")
        datatwo = dataone.replace("]", "")
        datathree = datatwo.replace("'", "")
        time.sleep(0.5)
        display.writelines(bytes(str(datathree) + "\n", 'utf-8'))
        time.sleep(0.5)
        print("Websocket Receive: " + str(datathree)) # Only for debugging


def sendWS(command):
    SendGcode = {
        "jsonrpc": "2.0",
        "method": "printer.gcode.script",
        "params": {
            "script": command
        },
        "id": 7466}
    ws.send(json.dumps(SendGcode))
    print("Websocket Send: " + str(command)) # Only for debugging


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
