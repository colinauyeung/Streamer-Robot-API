import serial
import pyrebase
import time
import json
from pathlib import Path

cwd = Path.cwd()
configfile = cwd / "config.json"

with open(configfile) as f:
    data = json.load(f)

config = data["config"]

serialport = data['arduinoport']

ser = serial.Serial(serialport)
print(ser.name)
state = [0, 0, 0]

firebase = pyrebase.initialize_app(config)

db = firebase.database()

t1 = time.time()

while True:
    line = ser.readline().decode("utf-8")
    for i in range (0,3):
        if line[i] == "0":
            state[i] = 0
        else:
            state[i] = 1
    print(line)

    data = db.child("controlheld").update(
        {"left": state[0], "right": state[1], "direct": state[2]})