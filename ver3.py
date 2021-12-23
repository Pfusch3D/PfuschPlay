import websocket
#import threading
#from time import sleep
from multiprocessing import Process

Status = False

def on_message(ws, message):
    print("Neue Nachricht")


def on_close(ws):
    print("### closed ###")

def on_open(ws):
    global Status
    Status = True


if __name__ == "__main__":
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp(
        "ws://localhost/websocket", on_open=on_open ,on_message=on_message, on_close=on_close)
    #ws = threading.Thread(target=ws.run_forever)
    Process(target=ws.run_forever).start()
    #ws.start()

    while Status:
        print("Hey hier kommt der TFT Code hin")

