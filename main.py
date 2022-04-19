import serialConnector
import websocketConnector
import time
import configparser
import sys
import datetime


config = configparser.RawConfigParser(inline_comment_prefixes='#')
config.read(str(sys.argv[1]))

displaytype = str(config["display"]["type"])
serialport = str(config["display"]["serial"])
baudrate = int(config["display"]["baudrate"])
moonraker_url = str(config["display"]["moonraker_url"])
preheatPLA = str(config["display"]["preheat_pla"]).split(",")
preheatABS = str(config["display"]["preheat_abs"]).split(",")
pfuschplayVersion = "BETA"

display = serialConnector.Serial(serialport, baudrate)
websocket = websocketConnector.Websocket(moonraker_url)


def checkCommand(command):
    if command == "A0":  # GET HOTEND TEMP
        request = {"extruder": ["temperature"]}
        response = websocket.getObjectStatus(request)
        temp = str(round(response["extruder"]["temperature"]))
        display.writeDisplay("A0V " + temp)

    elif command == "A1":  # GET HOTEND TARGET TEMP
        request = {"extruder": ["target"]}
        response = websocket.getObjectStatus(request)
        temp = str(round(response["extruder"]["target"]))
        display.writeDisplay("A1V " + temp)

    elif command == "A2":  # GET HEATBED TEMP
        request = {"heater_bed": ["temperature"]}
        response = websocket.getObjectStatus(request)
        temp = str(round(response["heater_bed"]["temperature"]))
        display.writeDisplay("A2V " + temp)

    elif command == "A3":  # GET HEATBED TARGET TEMP
        request = {"heater_bed": ["target"]}
        response = websocket.getObjectStatus(request)
        temp = str(round(response["heater_bed"]["target"]))
        display.writeDisplay("A3V " + temp)

    elif command == "A4":  # GET FAN SPEED
        request = {"fan": ["speed"]}
        response = websocket.getObjectStatus(request)
        speed = str(round(response["fan"]["speed"] * 100))
        display.writeDisplay("A4V " + speed)

    elif command == "A5":  # GET POSITION
        request = {"motion_report": ["live_position"]}
        response = websocket.getObjectStatus(request)["motion_report"]["live_position"]
        positionX = str(response[0])
        positionY = str(response[1])
        positionZ = str(response[2])
        display.writeDisplay(
            "A5V X: " + positionX + " Y: " + positionY + " Z: " + positionZ
        )

    elif command == "A7":  # GET PRINT TIME
        request = {"print_stats": ["total_duration", "state"]}
        response = websocket.getObjectStatus(request)["print_stats"]
        printtime_seconds = round(response["total_duration"])
        printtime = str(datetime.timedelta(seconds=printtime_seconds)).split(":")
        status = str(response["state"])
        print(printtime)
        if status == "printing":
            display.writeDisplay("A7V " + printtime[0] + "H " + printtime[1] + "M")
        else:
            display.writeDisplay("A7V 999:999")

    elif command == "A9":  # PAUSE PRINT
        websocket.print("pause")

    elif command == "A10":  # RESUME PRINT
        websocket.print("resume")

    elif command == "A11":  # STOP PRINT
        websocket.print("cancel")
        display.writeDisplay("J16")

    elif command == "A12":  # KILL PRINTER
        websocket.sendCommand("M112")

    elif "A16" in command:  # SET NOZZLE TEMPERATURE
        if "S" in command:
            temp = str(command.split("S")[1])
        elif "C" in command:
            temp = str(command.split("C")[1])
        else:
            return
        websocket.sendCommand("SET_HEATER_TEMPERATURE HEATER=extruder TARGET=" + temp)

    elif "A17" in command:  # SET HEATBED TEMPERATURE
        if "S" in command:
            temp = str(command.split("S")[1])
        else:
            return
        websocket.sendCommand("SET_HEATER_TEMPERATURE HEATER=heater_bed TARGET=" + temp)

    elif "A18" in command:  # SET FAN SPEED
        if "S" in command:
            speed = str(round(int(command.split("S")[1]) * 255 / 100))
        else:
            return
        websocket.sendCommand("M106 S" + speed)

    elif command == "A19":  # TURN STEPPERS OFF
        websocket.sendCommand("M18")

    elif "A21" in command:  # HOME PRINTER
        if command == "A21 C":
            websocket.sendCommand("G28")
        elif command == "A21 X":
            websocket.sendCommand("G28 X")
        elif command == "A21 Y":
            websocket.sendCommand("G28 Y")
        elif command == "A21 Z":
            websocket.sendCommand("G28 Z")

    elif "A22" in command:  # MOVE AXIS
        if "X" in command:
            value = command.split("X")[1].split("F")
            params = "G91" + "\n" + "G1 X" + value[0] + " F" + value[1] + "\n" + "G90"
        elif "Y" in command:
            value = command.split("Y")[1].split("F")
            params = "G91" + "\n" + "G1 Y" + value[0] + " F" + value[1] + "\n" + "G90"
        elif "Z" in command:
            value = command.split("Z")[1].split("F")
            params = "G91" + "\n" + "G1 Z" + value[0] + " F" + value[1] + "\n" + "G90"
        elif "E" in command:
            value = command.split("E")[1].split("F")
            params = "G1 E0"  # !!! Todo: Check absolute/relative extrusion and extrude than in relative mode. After this switch to the mode before.
        else:
            return
        websocket.sendCommand(params)

    elif command == "A23":  # PREHEAT PLA
        websocket.sendCommand("SET_HEATER_TEMPERATURE HEATER=extruder TARGET=" + preheatPLA[0] + "\n" + "SET_HEATER_TEMPERATURE HEATER=heater_bed TARGET=" + preheatPLA[1])

    elif command == "A24":  # PREHEAT ABS
        websocket.sendCommand("SET_HEATER_TEMPERATURE HEATER=extruder TARGET=" + preheatABS[0] + "\n" + "SET_HEATER_TEMPERATURE HEATER=heater_bed TARGET=" + preheatABS[1])

    elif command == "A25":  # COOL DOWN
        websocket.sendCommand("TURN_OFF_HEATERS")
        display.writeDisplay("J12")

    elif command == "A33":
        display.writeDisplay("J33 PFUSCHPLAY " + pfuschplayVersion)

display.connectDisplay()
while True:
    data = display.readDisplayData()
    checkCommand(data)
    # while True:
    #     try:
    #         data = display.readDisplayData()
    #         checkCommand(data)
    #     except:
    #         try:
    #             display.connectDisplay()
    #         except:
    #             print("Display nicht erreichbar - Reconnect in 2 Sekunden")
    #             time.sleep(2)
