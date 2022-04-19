import serial


class Serial:
    def __init__(self, address, baudrate):
        self.address = address
        self.baudrate = baudrate
        self.display = serial.Serial()

    def connectDisplay(self):
        self.display.baudrate = self.baudrate
        self.display.port = self.address
        self.display.open()

    def writeDisplay(self, data):
        self.display.write((data + "\n").encode())

    def readDisplayData(self):
        data = (
            self.display.readline().decode("utf-8").replace("\r", "").replace("\n", "")
        )
        return data
