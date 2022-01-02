module.exports = (currentData, display, connection) => {
    const end = "\r\n"
    if (data == "A0") {
        display.write("A0V" + currentData.Nozzle_Temperature + end);
    } else if (data == "A1") {
        display.write("A1V" + currentData.Nozzle_Target_Temperature + end);
    } else if (data == "A2") {
        display.write("A2V" + currentData.Printbed_Temperature + end);
    } else if (data == "A3") {
        display.write("A3V" + currentData.Printbed_Target_Temperature + end);
    } else if (data == "A4") {
        display.write("" + end);
    } else if (data == "A5") {
        display.write("A5V X:" + currentData.Position_X + " Y:" + currentData.Position_Y + " Z:" + currentData.Position_Z + end);
    } else if (data == "A6") {
        display.write("A6V " + currentData.Print_Progress + end);
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
        display.write("A7V " + time + end)
    } else if (data == "A20") {
        display.write("" + end);
    } else {
        return 1;
    }
}