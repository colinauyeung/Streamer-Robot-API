# adapted from https://www.youtube.com/watch?v=UquTAf_9dVA

import cv2
import cv2.aruco as aruco
import numpy as np
import pyrebase
import json
from pathlib import Path
import sys, time, math

cwd = Path.cwd()
configfile = cwd / "config.json"

with open(configfile) as f:
    data = json.load(f)

config = data["config"]
camera = data["camera_number"]


id_find =  132
mark_size = 2

calib_path = ""
cam_matrix = np.loadtxt("calmatrx.txt", delimiter=",")
cam_distortion = np.loadtxt(calib_path + "caldel.txt", delimiter=",")

R_flip = np.zeros((3,3), dtype=np.float)
R_flip[0,0] = 1.0
R_flip[1,1] = -1.0
R_flip[2,2] = -1.0

aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_ARUCO_ORIGINAL)
para = aruco.DetectorParameters_create()

cap = cv2.VideoCapture(camera)

firebase = pyrebase.initialize_app(config)

db = firebase.database()


pollrate = db.child('pollrate').get().val()
t1 = time.time()
while True:
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    corners, ids, rejected = aruco.detectMarkers(image=gray, dictionary=aruco_dict, parameters=para, cameraMatrix=cam_matrix, distCoeff=cam_distortion)
    ls = {}
    ls["ID130"] = {"x": 0, "y": 0}
    ls["ID140"] = {"x": 0, "y": 0}
    if ids is not None:
        #ret = aruco.estimatePoseSingleMarkers(corners, mark_size, cam_matrix, cam_distortion)

        #rvec, tvec = ret[0][0,0,:], ret[1][0,0,:]

        for i in range(0, len(corners)):
            if ids[i][0] == 130 or ids[i][0] == 140:
                ls["ID{id}".format(id = ids[i][0])] = {"x":corners[i][0][0][0].item(), "y":corners[i][0][0][1].item()}

        print(ls)



        aruco.drawDetectedMarkers(frame, corners)
        #aruco.drawAxis(frame, cam_matrix, cam_distortion, rvec, tvec, 10)

    cv2.imshow('frame', frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

    if time.time() - t1 >= pollrate:
        ping = db.child("ping").child("visaruco").child("ping").get()
        print(ping.val())
        if ping.val() == "pong":
            data = db.child("handvis").update(ls)
            db.child("ping").child("visaruco").update({"ping": "ping"})
        t1 = time.time()
        pollrate = db.child('pollrate').get().val()

