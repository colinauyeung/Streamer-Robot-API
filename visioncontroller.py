# adapted from https://www.youtube.com/watch?v=wlT_0fhGrGg

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

boundary = ([86, 31, 4], [220, 88, 50])
cap = cv2.VideoCapture(camera)
img1 = cv2.imread('controller.jpg', 1)

orb = cv2.ORB_create()
kp1, des1 = orb.detectAndCompute(img1, None)

bf = cv2.BFMatcher_create(cv2.NORM_HAMMING, crossCheck=True)
ret, frame = cap.read()

agg = {"x": [], "y": [], "count": 1}

def updateagg (x,y):
    if agg["count"] > 10:
        agg["x"].pop(0)
        agg["y"].pop(0)
        agg["count"] = agg["count"] -1
    agg["x"].append(x)
    agg["y"].append(y)
    agg["count"] = agg["count"] + 1

def avg(ls):
    avg = 0
    count = 1
    for i in ls:
        count=count+1
        avg = avg + i
    return avg/count


firebase = pyrebase.initialize_app(config)

db = firebase.database()

pollrate = db.child('pollrate').get().val()
t1 = time.time()
def drawBox(img):
    x = avg(agg["x"])
    y = avg(agg["y"])
    w,h = 10,10
    cv2.rectangle(img, (int(x), int(y)), (int(x+w), int(y+h)), (255, 0, 255), 3, 1)

while(True):
    timer = cv2.getTickCount()
    # Capture frame-by-frame
    ret, frame = cap.read()

    kp2, des2 = orb.detectAndCompute(frame, None)

    matches = bf.match(des1, des2)
    matches = sorted(matches, key= lambda x:x.distance)
    remat = []
    for mat in matches[:10]:
        if mat.distance <= 30:
            remat.append(mat)
            (x,y) = kp2[mat.trainIdx].pt
            updateagg(x,y)


    drawBox(frame)

    print(agg)

    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if time.time() - t1 >= pollrate:
        ping = db.child("ping").child("vis").child("ping").get()
        if ping.val() == "pong":
            data = db.child("controlvis").update({"x":str(avg(agg["x"])), "y":str(avg(agg["y"]))})
            db.child("ping").child("vis").update({"ping": "ping"})
        t1 = time.time()
        pollrate = db.child('pollrate').get().val()


# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()