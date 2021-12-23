import websocket
#import threading
#from time import sleep
from multiprocessing import Process


def on_message(ws, message):
    print("Neue Nachricht")


def on_close(ws):
    print("### closed ###")


if __name__ == "__main__":
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp(
        "ws://localhost/websocket", on_message=on_message, on_close=on_close)
    #ws = threading.Thread(target=ws.run_forever)
    Process(target=ws.run_forever).start()
    #ws.start()

    while ws.connected:
        print("Hey hier kommt der TFT Code hin")
