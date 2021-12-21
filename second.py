import serial

PfuschPlay = {
    # /dev/ttyAMA0 = GPIO UART.
    "serialPort": "/dev/ttyAMA0",
    # Default baudrate. General baudrates: 9600, 115200, 250000
    "baudrate": "115200",
    # Only change URL when you run PfuschPlay on other Linux Machine.
    "websocketURL": "ws://localhost/websocket"
}

display = serial.Serial()
display.baudrate = PfuschPlay["baudrate"]
display.port = PfuschPlay["serialPort"]
display.open()

while True:
    display.write(b"Hello World sagt das Python Programm")