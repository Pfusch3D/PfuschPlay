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


def checkS():
    if (display.in_waiting() > 0):
        data = display.readline().rstrip().decode("ascii")
        print("TFT Input: " + data)
        time.sleep(0.01)
        return data


def sendWS(command):
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
                new = data["params"]
                print(new[:-2])


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

    ws.run_forever()
    while True:
        checkS()
