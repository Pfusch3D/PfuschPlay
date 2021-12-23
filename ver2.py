from clean import sendS
import websocket
import serial
import json
import config
import _thread
import time

display = serial.Serial()
# Load baudrate from config file:
display.baudrate = config.PfuschPlay["baudrate"]
# Load port from config file:
display.port = config.PfuschPlay["serialPort"]
# Wait for Bootloader of TFT
time.sleep(2)
display.open()


def convertASCII(input):
    ascii_values = [ord(character) for character in input]
    return ascii_values


def checkS():
    data = display.readline().rstrip().decode("ascii")
    print("TFT Input: " + data)
    time.sleep(0.01)
    sendWS(data)


def sendWS(ws, command):
    SendGcode = {
        "jsonrpc": "2.0",
        "method": "printer.gcode.script",
        "params": {
            "script": command
        },
        "id": 7466}
    ws.send(json.dumps(SendGcode))


def on_message(ws, message):
    data = json.loads(message)
    if "method" in data:
        if data["method"] == "notify_gcode_response":
            if "params" in data:
                data = str(data["params"])
                data = data[3:-2] + "\r\n"
                print(data)
                display.write(convertASCII(data))
                time.sleep(0.01)


def on_error(ws, error):
    print("Fehler: " + error)


def on_open(ws):
    print("Websocket Verbindung hergestellt.")


if __name__ == "__main__":
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp("ws://localhost/websocket",
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error)
    counter = 0
    while True:
        if counter == 0:
            ws.run_forever()
            counter = 1
        checkS()
