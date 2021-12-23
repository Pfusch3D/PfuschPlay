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

def filterData(input):
    data = str(input)
    data = str(data[2:-2]).strip()
    return data

def receiveWS():

    ws_data = ws.recv()
    data = json.loads(ws_data)

    if "method" in data:
        if data["method"] == "notify_gcode_response":
            global emergency
            content = filterData(data["params"])
            if content == "!! Shutdown due to webhooks request":
                emergency = 1
            else:
                print("Jetzt kommen die True facts: " + content)
                return content


def sendS(command):
    global emergency
    if command and emergency == 0:
        data = command + "\r\n"
        display.write(convertASCII(data))
        time.sleep(0.01)

        print("Websocket Receive: " + str(data))  # Only for debugging
    else:
        print("Error. Vielleicht Emergency Stop?")


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
