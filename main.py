#!python3
import configparser
import sys
import serial
import websocket
import requests
import time
import json
import datetime

config = configparser.RawConfigParser()
config.read(str(sys.argv[1]))

displaytype = str(config["display"]["displaytype"])
serialport = str(config["display"]["serialport"])
baudrate = int(config["display"]["baudrate"])
moonraker_url = str(config["display"]["moonraker_url"])
display = serial.Serial()

connected = False


def connectDisplay():
    display.baudrate = baudrate
    display.port = serialport
    display.open()

def writeDisplay(data):
    display.write((data + "\n").encode())


def readDisplayData():
    data = display.readline().decode("utf-8").replace("\r", "").replace("\n", "")
    return data


def checkCommand(command):
    #print(command)
    if command == "A0":  # GET HOTEND TEMP
        url = moonraker_url + "/api/printer"
        r = requests.get(url)
        result = json.loads(r.text)
        temp = str(result["temperature"]["tool0"]["actual"])

        writeDisplay("A0V " + temp)

    elif command == "A1":  # GET HOTEND TARGET TEMP
        url = moonraker_url + "/api/printer"
        r = requests.get(url)
        result = json.loads(r.text)
        temp = str(round(result["temperature"]["tool0"]["target"]))

        writeDisplay("A1V " + temp)

    elif command == "A2":  # GET HEATBED TEMP
        url = moonraker_url + "/api/printer"
        r = requests.get(url)
        result = json.loads(r.text)
        temp = str(round(result["temperature"]["bed"]["actual"]))

        writeDisplay("A2V " + temp)

    elif command == "A3":  # GET HEATBED TARGET TEMP
        url = moonraker_url + "/api/printer"
        r = requests.get(url)
        result = json.loads(r.text)
        temp = str(round(result["temperature"]["bed"]["target"]))

        writeDisplay("A3V " + temp)

    elif command == "A4":  # GET FAN SPEED
        url = moonraker_url + "/printer/objects/query"
        params = {"fan": ""}
        r = requests.get(url, data=params)
        result = json.loads(r.text)
        speed = str(round(result["result"]["status"]["fan"]["speed"] * 100))

        writeDisplay("A4V " + speed)

    elif command == "A5":   # GET POSITION
        url = moonraker_url + "/printer/objects/query"
        params = {"motion_report": ""}
        r = requests.get(url, data=params)
        result = json.loads(r.text)
        position_x = str(result["result"]["status"]["motion_report"]["live_position"][0])
        position_y = str(result["result"]["status"]["motion_report"]["live_position"][1])
        position_z = str(result["result"]["status"]["motion_report"]["live_position"][2])
        writeDisplay("A5V X: " + position_x + " Y: " + position_y + " Z: " + position_z)

    elif command == "A6": # GET PRINT PROGRESS
        writeDisplay("A6V 0") # I do not know how to do this...

    elif command == "A7":
        url = moonraker_url + "/printer/objects/query"
        params = {"print_stats": ""}
        r = requests.get(url, data=params)
        result = json.loads(r.text)
        status = str(result["result"]["status"]["print_stats"]["state"])
        printtime_seconds = round(result["result"]["status"]["print_stats"]["total_duration"])
        printtime = str(datetime.timedelta(seconds=printtime_seconds)).split(":")
        if status == "printing":
            writeDisplay("A7V " + printtime[1] + "H " + printtime[2] + "M")
        else:
            writeDisplay("A7V 999:999")

    elif "A8" in command: # GET PRINT LIST
        writeDisplay("FN ")
        writeDisplay("test.gcode")
        writeDisplay("END") 

    elif command == "A9": # PAUSE PRINT
        url = moonraker_url + "/printer/print/pause"
        requests.post(url)

    elif command == "A10": # RESUME PRINT
        url = moonraker_url + "/printer/print/resume"
        requests.post(url)

    elif command == "A11": # STOP PRINT
        url = moonraker_url + "/printer/print/cancel"
        requests.post(url)
        writeDisplay("J16")
    
    elif command == "A12": # KILL PRINTER
        url = moonraker_url + "/printer/emergency_stop"
        requests.post(url)

    elif "A16" in command: # SET NOZZLE TEMPERATURE
        if "S" in command:
            temp = command.split("S")[1]
        elif "C" in command:
            temp = command.split("C")[1]
        else:
            return
        url = moonraker_url + "/printer/gcode/script"
        params = {"script": "SET_HEATER_TEMPERATURE HEATER=extruder TARGET=" + temp}
        requests.post(url, data=params)

    elif "A17" in command: # SET HEATBED TEMPERATURE
        if "S" in command:
            temp = command.split("S")[1]
        else:
            return
        url = moonraker_url + "/printer/gcode/script"
        params = {"script": "SET_HEATER_TEMPERATURE HEATER=heater_bed TARGET=" + temp}
        requests.post(url, data=params)

    elif "A18" in command: # SET FAN SPEED
        if "S" in command:
            speed = str(round(int(command.split("S")[1]) * 255 / 100))
        else:
            return
        url = moonraker_url + "/printer/gcode/script"
        params = {"script": "M106 S" + speed}
        requests.post(url, data=params)

    elif command == "A19":
        url = moonraker_url + "/printer/gcode/script"
        params = {"script": "M18"}
        requests.post(url, data=params)
        
    elif "A21" in command:
        url = moonraker_url + "/printer/gcode/script"
        if command == "A21 C":
            params = {"script": "G28"}
            requests.post(url, data=params)

        elif command == "A21 X":
            params = {"script": "G28 X"}
            requests.post(url, data=params)

        elif command == "A21 Y":
            params = {"script": "G28 Y"}
            requests.post(url, data=params)

        elif command == "A21 Z":
            params = {"script": "G28 Z"}
            requests.post(url, data=params)

    elif "A22" in command:
        url = moonraker_url + "/printer/gcode/script"
        if "X" in command:
            value = command.split("X")[1].split("F")
            params = {"script": "G91" + "\n" + "G1 X" + value[0] + " F" + value[1] + "\n" + "G90"}
        elif "Y" in command:
            value = command.split("Y")[1].split("F")
            params = {"script": "G91" + "\n" + "G1 Y" + value[0] + " F" + value[1] + "\n" + "G90"}
        elif "Z" in command:
            value = command.split("Z")[1].split("F")
            params = {"script": "G91" + "\n" + "G1 Z" + value[0] + " F" + value[1] + "\n" + "G90"}
        elif "E" in command:
            value = command.split("E")[1].split("F")
            params = {"script": "G1 E0"} # !!! Todo: Check absolute/relative extrusion and extrude than in relative mode. After this switch to the mode before.
        else:
            return
        requests.post(url, data=params)
        

if __name__ == "__main__":
    while True:
        try:
            data = readDisplayData()
            checkCommand(data)
        except:
            try:
                connectDisplay()
            except:
                print("Display nicht erreichbar - Reconnect in 2 Sekunden")
                time.sleep(2)
