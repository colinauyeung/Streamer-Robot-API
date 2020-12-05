import pyrebase
import random
import time

config = {
    "apiKey": "AIzaSyCfSSnLmj5KcoD6B4fgsgbiSsj_x3-o9Bc",
    "authDomain": "hri-bottuber.firebaseapp.com",
    "databaseURL": "https://hri-bottuber.firebaseio.com",
    "storageBucket": "hri-bottuber.appspot.com"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()
print(time.time())
time.sleep(1)
print(time.time())
while True:
    ping = db.child("ping").child("ping").get()
    if ping.val() == "pong":
        data = db.child("data").update({"h": str(random.randrange(1,10))})
        db.child("ping").update({"ping": "ping"})
    time.sleep(1)

