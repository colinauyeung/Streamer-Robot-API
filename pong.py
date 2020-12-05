# import requests
# import time
# while True:
#     ping = requests.get('https://hri-bottuber.firebaseio.com/ping.json').json()
#     if ping["ping"] == "ping":
#         req = requests.get('https://hri-bottuber.firebaseio.com/data.json')
#         requests.patch('https://hri-bottuber.firebaseio.com/ping.json', json={'ping': 'pong'})
#         print(req.json())
#         time.sleep(5)

# ping = requests.get("https://hri-bottuber.firebaseio.com/ping/ping.json")
# print(ping)
# print(ping.json())

# print({1: 0})
# firebase = 'https://hri-bottuber.firebaseio.com/'
# print('{url}controlhat.json'.format(url = firebase))
# from pathlib import Path
#
# print(Path.cwd())
import numpy as np
import cv2
import pyrebase
import time
import json
from pathlib import Path
import matplotlib.pyplot as plt

cwd = Path.cwd()
configfile = cwd / "config.json"

with open(configfile) as f:
    data = json.load(f)

config = data["config"]
camera = data["camera_number"]
print(type(camera))
print(camera)
