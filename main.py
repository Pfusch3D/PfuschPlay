import serial
import requests
import json


serialPort = "/dev/ttyAMA0"
baudrate = "115200"
moonrakerURL = "http://localhost:7125/api/printer/command"

display = serial.Serial()
display.baudrate = baudrate
display.port = serialPort
display.open()


def readData():
    data = display.readline().rstrip().decode("utf-8")
    # print(data)
    return data


def writeData(input):
    jdata = {"commands": [input]}
    requests.post(moonrakerURL, json=jdata)


def response():
    url = "http://localhost:7125/moonraker/api/response"
    headers = {'content-type': 'application/json'}

    payload = {
        "jsonrpc": "2.0",
        "method": "notify_gcode_response",
        "params": ["response message"]
    }
    res = requests.post(url, data=json.dumps(payload), headers=headers).json()
    assert res["result"] == "response message"


while True:
    r_data = readData()
    writeData(r_data)
    response()
