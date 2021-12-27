#!/usr/bin/node

const WebSocketClient = require('websocket').client;
const SerialPort = require('serialport');
const config = require('./config.json');
const parsers = SerialPort.parsers;


const display = new SerialPort(config.SerialPort, {
    baudRate: config.SerialBaudrate,
    autoOpen: true
});

const parser = new parsers.Readline({
    delimiter: '\r\n',
});

display.pipe(parser);

const ws = new WebSocketClient();

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
    Print_Progress: ""

};
var commandResponse;

display.write("J00" + "\r\n");
display.write("J12" + "\r\n");




console.log("PfuschPlay was started - PfuschPlay wurde gestartet")

ws.on('connect', function (connection) {
    connection.on('message', function (message) {
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
            currentData.Print_Progress = data.result.status.virtual_sdcard.progress * 100

        } else if (data.method == "notify_gcode_response") {
            commandResponse = data.params.toString()
            display.write(commandResponse.trim() + "\r\n")
            console.log(commandResponse)
        }
    });

    parser.on('data', function (data) {
        console.log("Display Data: " + data);
        if (data == "A0") {
            display.write("A0V" + currentData.Nozzle_Temperature + "\r\n");
        } else if (data == "A1") {
            display.write("A1V" + currentData.Nozzle_Target_Temperature + "\r\n");
        } else if (data == "A2") {
            display.write("A2V" + currentData.Printbed_Temperature + "\r\n");
        } else if (data == "A3") {
            display.write("A3V" + currentData.Printbed_Target_Temperature + "\r\n");
        } else if (data == "A4") {
            display.write("" + "\r\n");
        } else if (data == "A5") {
            display.write("A5V X:" + currentData.Position_X + " Y:" + currentData.Position_Y + " Z:" + currentData.Position_Z + "\r\n");
        } else if (data == "A6") {
            display.write("A6V " + currentData.progress +  "\r\n");
        } else if (data == "A7") {
            function timeConvert(n) {
                var num = n;
                var hours = (num / 60);
                var rhours = Math.floor(hours);
                var minutes = (hours - rhours) * 60;
                var rminutes = Math.round(minutes);
                return rhours + "H " + rminutes + " M";
            }
            let time = timeConvert(currentData.Print_Time)
            display.write("A7V " + time + "\r\n")
        } else if (data == "A12") {
            let sample = {
                "jsonrpc": "2.0",
                "method": "printer.emergency_stop",
                "id": 4564
            }
            connection.send(JSON.stringify(sample));
        } else if (data == "A20") {
            display.write("" + "\r\n");
        } else {
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
    setInterval(Get_Temp_Data, 500);
})

ws.on('connectFailed', function (error) {
    console.log('Connect Error: ' + error.toString());
});


ws.connect(config.WebSocketURL);