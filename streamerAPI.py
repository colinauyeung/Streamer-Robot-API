import pyrebase
import time
import json
import threading
from pathlib import Path

class streamertracking:

    firebase = None
    db = None
    controllerdata = None
    visiondata = None
    arucodata = None
    mousedata = None
    pollrate = 1
    controllerdata_ava = threading.Event()
    visiondata_ava = threading.Event()
    arucodata_ava = threading.Event()
    mousedata_ava = threading.Event()

    def __init__(self):
        cwd = Path.cwd()
        configfile = cwd / "config.json"
        with open(configfile) as f:
            data = json.load(f)

        config = data["config"]
        self.firebase = pyrebase.initialize_app(config)
        self.db = self.firebase.database()
        self.pollrate = self.db.child('pollrate').get().val()
        return



    def pollcontroller(self):
        self.db.child('ping').child('controller').update({"ping": "pong"})
        while True:
            ping = self.db.child('ping').child('controller').child('ping').get().val() == "ping"
            if ping:
                self.controllerdata = self.db.child("joystick").get().val()
                self.controllerdata_ava.set()
                return
            time.sleep(self.pollrate/4)

    def pollvision(self):
        self.db.child('ping').child('vis').update({"ping": "pong"})
        while True:
            ping = self.db.child('ping').child('vis').child('ping').get().val() == "ping"
            if ping:
                self.visiondata = self.db.child("controlvis").get().val()
                self.visiondata_ava.set()
                return
            time.sleep(self.pollrate/4)

    def pollaruco(self):
        self.db.child('ping').child('visaruco').update({"ping": "pong"})
        while True:
            ping = self.db.child('ping').child('visaruco').child('ping').get().val() == "ping"
            if ping:
                self.arucodata = self.db.child("handvis").get().val()
                self.arucodata_ava.set()
                return
            time.sleep(self.pollrate/4)

    def pollmouse(self):
        self.db.child('ping').child('mouse').update({"ping": "pong"})
        while True:
            ping = self.db.child('ping').child('mouse').child('ping').get().val() == "ping"
            if ping:
                self.mousedata = self.db.child("mousepos").get().val()
                self.mousedata_ava.set()
                return
            time.sleep(self.pollrate/4)

    def getJoystick(self):
        self.db.child('ping').child('controller').update({"ping": "pong"})
        thread = threading.Thread(target=self.pollcontroller)
        thread.start()
        self.controllerdata_ava.wait()
        self.controllerdata_ava.clear()
        return self.controllerdata

    def getMouse(self):
        thread = threading.Thread(target=self.pollmouse)
        thread.start()
        self.mousedata_ava.wait()
        self.mousedata_ava.clear()
        return self.mousedata

    def getVision(self):
        thread = threading.Thread(target=self.pollvision)
        thread.start()
        self.visiondata_ava.wait()
        self.visiondata_ava.clear()
        return self.visiondata

    def getAruco(self):
        thread = threading.Thread(target=self.pollaruco())
        thread.start()
        self.arucodata_ava.wait()
        self.arucodata_ava.clear()
        return self.arucodata

    def getHeldData(self):
        return self.db.child("controlheld").get().val()

    def getDPad(self):
        return self.db.child("controlhat").get().val()

    def getButtons(self):
        return self.db.child("controldpad").get().val()

    def updatePollrate(self, rate):
        self.db.update({"pollrate": rate})

if __name__ == "__main__":
    tracking = streamertracking()
    print(tracking.getHeldData())
