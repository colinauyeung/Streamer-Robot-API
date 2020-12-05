#code based on code from https://stackoverflow.com/questions/3698635/getting-cursor-position-in-python

from ctypes import windll, Structure, c_long, byref
import time
import requests

import json
from pathlib import Path




class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]

def queryMousePosition():
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return { "x": pt.x, "y": pt.y}

cwd = Path.cwd()
configfile = cwd / "config.json"

with open(configfile) as f:
    data = json.load(f)

firebase = data['firebaseurl']

pollrate = requests.get("{url}pollrate.json".format(url=firebase)).json()


t1 = time.time()
while True:
    pos = queryMousePosition()
    print(pos)

    if time.time() - t1 >= pollrate:
        ping = requests.get("{url}ping/mouse/ping.json".format(url=firebase))
        if ping.json() == "pong":
            requests.patch(
                '{url}mousepos.json'.format(url=firebase),
                json={"x":pos["x"], "y":pos["y"]})
            requests.patch('{url}ping/mouse.json'.format(url=firebase),
                           json={'ping': 'pong'})
            t1 = time.time()

        pollrate = requests.get(
            "{url}pollrate.json".format(url=firebase)).json()
