#!/usr/bin/node

const WebSocketClient = require("websocket").client;
const SerialPort = require("serialport");
const config = require("./config.json");
const parsers = SerialPort.parsers;


const display = new SerialPort(config.SerialPort, {
    baudRate: config.SerialBaudrate,
    autoOpen: true
});

const parser = new parsers.Readline({
    delimiter: "\r\n"
});

display.pipe(parser);

const ws = new WebSocketClient();

var commandsPath;
var startPath;

if (config.DisplayType == "Anycubic") {
    commandsPath = "./TFT_Anycubic/commands";
    startPath = "./TFT_Anycubic/start";
} else if (config.DisplayType == "BTT/MKS") {
    commandsPath = "./TFT_BTTMKS/commands";
    startPath = "./TFT_BTTMKS/start";
} else if (config.DisplayType == "Custom") {
    commandsPath = "./TFT_Custom/commands";
    startPath = "./TFT_Custom/start";
} else {
    console.log("Display Typ nicht gefunden. Bitte DisplayType in config.json überprüfen.")
    console.log("Display type not found. Please check DisplayType in config.json")
    process.exit(1)
}

const commands = require(commandsPath);
const start = require(startPath)

var currentData = {
    Nozzle_Temperature: "",
    Nozzle_Target_Temperature: "",
    Printbed_Temperature: "",
    Printbed_Target_Temperature: "",
    Position_X: "",
    Position_Y: "",
    Position_Z: "",
    Speed_Factor: "",
    Extrude_Factor: "",
    Print_Time: "",
    Print_Progress: "",
    commandResponse: ""

};
console.log("PfuschPlay wurde gestartet")
console.log("PfuschPlay was started")

start(display)

ws.on("connect", function (connection) {
    connection.on("message", function (message) {
        let data = message.utf8Data;
        data = JSON.parse(data);
        //console.log(data)
        if (data.id == 2313) {
            currentData.Nozzle_Temperature = data.result.extruder.temperatures[data.result.extruder.temperatures.length - 1];
            currentData.Nozzle_Target_Temperature = data.result.extruder.targets[data.result.extruder.targets.length - 1];

            currentData.Printbed_Temperature = data.result.heater_bed.temperatures[data.result.heater_bed.temperatures.length - 1];
            currentData.Printbed_Target_Temperature = data.result.heater_bed.targets[data.result.heater_bed.targets.length - 1];

            //console.log("Nozzle + Printbed: " + currentData.Nozzle_Temperature + " : " + currentData.Printbed_Temperature) //Debugging
            //console.log(data)
        } else if (data.id == 4654) {

            currentData.Position_X = data.result.status.gcode_move.position[0].toFixed()
            currentData.Position_Y = data.result.status.gcode_move.position[1].toFixed()
            currentData.Position_Z = data.result.status.gcode_move.position[2].toFixed()

            currentData.Speed_Factor = data.result.status.gcode_move.speed_factor
            currentData.Extrude_Factor = data.result.status.gcode_move.extrude_factor

        } else if (data.id == 5664) {
            currentData.Print_Time = parseInt(data.result.status.print_stats.total_duration) / 60
            currentData.Print_Progress = (data.result.status.virtual_sdcard.progress * 100).toFixed()

        } else if (data.method == "notify_gcode_response") {
            commandResponse = data.params.toString()
            display.write(commandResponse.trim() + "\r\n")
            //console.log(commandResponse.trim())
        }
    });

    parser.on("data", function (DisplayData) {
        //console.log("Display Data: " + data);
        let status = commands(DisplayData, currentData, display)
        if (status == 1) {
            let sample = {
                "jsonrpc": "2.0",
                "method": "printer.gcode.script",
                "params": {
                    "script": data
                },
                "id": 7466
            }
            connection.send(JSON.stringify(sample));
        }

    })

    function Get_Temp_Data() {
        let sample1 = {
            "jsonrpc": "2.0",
            "method": "server.temperature_store",
            "id": 2313
        };
        connection.send(JSON.stringify(sample1));

        let sample2 = {
            "jsonrpc": "2.0",
            "method": "printer.objects.query",
            "params": {
                "objects": {
                    "gcode_move": ["speed_factor", "position", "extrude_factor"],
                }
            },
            "id": 4654
        }
        connection.send(JSON.stringify(sample2));

        let sample3 = {
            "jsonrpc": "2.0",
            "method": "printer.objects.query",
            "params": {
                "objects": {
                    "virtual_sdcard": ["progress"],
                    "print_stats": ["total_duration"]
                }
            },
            "id": 5664
        }
        connection.send(JSON.stringify(sample3));

    };
    setInterval(Get_Temp_Data, 500); // Request ever half second new Data for currentData
})

ws.on("connectFailed", function (error) {
    console.log("ALAAARM! Error: " + error.toString());
});


ws.connect(config.WebSocketURL);