import websocket
import serial
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
    print(message)

def on_error(ws, error):
    print(error)

def on_open(ws):
    # def run(*args):
    #     for i in range(3):
    #         time.sleep(1)
           
    #     time.sleep(1)
    #     #ws.close()
    #     print("thread terminating...")
    # _thread.start_new_thread(run, ())
    print("Websocket gestartet")

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost/websocket",
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error)

    ws.run_forever()

