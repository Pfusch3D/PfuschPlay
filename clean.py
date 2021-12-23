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
emergency = 2  # 1 --> active, 2 --> inactive

ws = websocket.WebSocket()
# Load websocket URL from config file:
ws.connect(config.PfuschPlay["websocketURL"])




def checkEmergency(status=0):
    global emergency
    if status == 1:
        emergency = 1
    elif status == 2:
        emergency = 2
    elif status == 0:
        return emergency


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
            content = filterData(data["params"])
            if content == "!! Shutdown due to webhooks request":
                checkEmergency(status=1)
            print("Jetzt kommen die True facts: " + content)
            return content


def sendS(command):
    if command:
        if checkEmergency() is 2:
            data = command + "\r\n"
            display.write(convertASCII(data))
            time.sleep(0.01)

            print("Websocket Receive: " + str(data))  # Only for debugging
        elif checkEmergency() is 1:
            print("Error ich darf nichts senden!")


def sendWS(command):
    if command:
        if checkEmergency() is 2:
            SendGcode = {
                "jsonrpc": "2.0",
                "method": "printer.gcode.script",
                "params": {
                    "script": command
                },
                "id": 7466}
            print("Bypass!")
            ws.send(json.dumps(SendGcode))

            print("Websocket Send: " + str(command))  # Only for debugging
        elif checkEmergency() is 1:
            print("Error ich darf auch nichts senden!")


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

checkEmergency(status=2)


Process(target=rec).start()
Process(target=sen).start()

# while True:
#     x = receiveS()
#     sendWS(x)
#     # time.sleep(0.5)
#     y = receiveWS()
#     sendS(y)
