import websocket
import json
import random


class Websocket:
    def __init__(self, address):
        self.address = address
        self.ws = websocket.WebSocket()
        self.ws.connect(self.address)

    def randomId(self):
        id = int(random.random() * 10000000000)
        return id

    def reconnect(self):
        try:
            self.ws.close()
            self.ws.connect(self.address)
            return True
        except:
            return False

    def sendCommand(self, command):
        data = {
            "jsonrpc": "2.0",
            "method": "printer.gcode.script",
            "params": {"script": command},
            "id": self.randomId(),
        }
        self.ws.send(json.dumps(data))
        id = 0
        while id != data["id"] or id < 10:
            receive = self.ws.recv()
            receive = json.loads(receive)
            if "id" in receive:
                id = receive["id"]
                return receive
            else:
                id += 1
        return False

    def getObjects(self):
        data = {
            "jsonrpc": "2.0",
            "method": "printer.objects.list",
            "id": self.randomId(),
        }
        self.ws.send(json.dumps(data))
        id = 0
        while id != data["id"] or id < 10:
            receive = self.ws.recv()
            receive = json.loads(receive)
            if "id" in receive:
                id = receive["id"]
                return receive["result"]["objects"]
            else:
                id += 1
        return False

    def getObjectStatus(self, objects):
        data = {
            "jsonrpc": "2.0",
            "method": "printer.objects.query",
            "params": {"objects": objects},
            "id": self.randomId(),
        }
        self.ws.send(json.dumps(data))
        id = 0
        while id != data["id"] or id < 10:
            receive = self.ws.recv()
            receive = json.loads(receive)
            if "id" in receive:
                id = receive["id"]
            else:
                id += 1
        if data["id"] == id and "result" in receive:
            return receive["result"]["status"]
        else:
            return False

    def print(self, command):
        data = {
            "jsonrpc": "2.0",
            "method": "printer.print." + command,
            "id": self.randomId(),
        }
        self.ws.send(json.dumps(data))
        id = 0
        while id != data["id"] or id < 10:
            receive = self.ws.recv()
            receive = json.loads(receive)
            if "id" in receive:
                id = receive["id"]
                return True
            else:
                id += 1
        return False
