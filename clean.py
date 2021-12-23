from multiprocessing import Process
import websocket
import serial
import json
import config
import time

display = serial.Serial()
# Load baudrate from config file:
display.baudrate = config.PfuschPlay["baudrate"]
# Load port from config file:
display.port = config.PfuschPlay["serialPort"]
# Wait for Bootloader of TFT
time.sleep(2)
display.open()

ws = websocket.WebSocket()
# Load websocket URL from config file:
ws.connect(config.PfuschPlay["websocketURL"])

emergency = 0


def convertASCII(input):
    ascii_values = [ord(character) for character in input]
    return ascii_values


def receiveWS():
    global emergency
    print(emergency)
    emergency = 1
    print(emergency)

    ws_data = ws.recv()
    data = json.loads(ws_data)

    if "method" in data:
        if data["method"] == "notify_gcode_response":
            return data["params"]


def sendS(command):
    if command:
        data = str(command)
        data = str(data[3:-2]) + "\r\n"
        display.write(convertASCII(data))
        time.sleep(0.01)

        print("Websocket Receive: " + str(data))  # Only for debugging


def sendWS(command):
    SendGcode = {
        "jsonrpc": "2.0",
        "method": "printer.gcode.script",
        "params": {
            "script": command
        },
        "id": 7466}

    ws.send(json.dumps(SendGcode))

    print("Websocket Send: " + str(command))  # Only for debugging


def receiveS():
    data = display.readline().rstrip().decode("UTF-8")
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

# while True:
#     x = receiveS()
#     sendWS(x)
#     # time.sleep(0.5)
#     y = receiveWS()
#     sendS(y)
