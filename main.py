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



def convertASCII(input):
    ascii_values = [ord(character) for character in input]
    return ascii_values


def filterData(input):
    data = str(input)
    data = str(data[2:-2]).strip()
    return data


def receiveWS():
    global shutdown
    ws_data = ws.recv()
    data = json.loads(ws_data)
    if "method" in data:
        if data["method"] == "notify_gcode_response":
            content = filterData(data["params"])
            return content


def sendS(command):
    if command:
        data = command + "\r\n"
        display.write(convertASCII(data))
        time.sleep(0.01) # Protect against overload



def sendWS(command):
    if command:
        SendGcode = {
            "jsonrpc": "2.0",
            "method": "printer.gcode.script",
            "params": {
                "script": command
            },
            "id": 7466}
        ws.send(json.dumps(SendGcode))


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
        print()
        sendS(y)


Process(target=rec).start()
Process(target=sen).start()

