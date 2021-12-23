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


def on_message(ws, message):
    data = json.loads(message)
    if "method" in data:
        if data["method"] == "notify_gcode_response":
            if "params" in data:
                print("Hello World")


def on_error(ws, error):
    print("Fehler: " + error)


def on_open(ws):
    print("Websocket Verbindung hergestellt.")


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost/websocket",
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error)

    ws.run_forever()
