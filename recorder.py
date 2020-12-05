import pyrebase
import time

config = {
    "apiKey": "AIzaSyCfSSnLmj5KcoD6B4fgsgbiSsj_x3-o9Bc",
    "authDomain": "hri-bottuber.firebaseapp.com",
    "databaseURL": "https://hri-bottuber.firebaseio.com",
    "storageBucket": "hri-bottuber.appspot.com"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()

t1 = time.time()


pollrate = db.child('pollrate').get().val()
file = open("log.txt", "w+")
file.close()



def boolToInt(b):
    if b:
        return 1
    else:
        return 0

while True:
    if time.time() - t1 >= pollrate:

        print
        if db.child("ping").child("vis").child("ping").get().val() == "ping" \
                and db.child("ping").child("mouse").child("ping").get().val() == "ping" \
                and db.child("ping").child("controller").child("ping").get().val() == "ping":
            dpad = db.child("controldpad").get().val()
            hat = db.child("controlhat").get().val()
            held = db.child("controlheld").get().val()
            vis = db.child("controlvis").get().val()
            ID130 = db.child("handvis").child("ID130").get().val()
            ID140 = db.child("handvis").child("ID140").get().val()
            db.child("ping").child("vis").update({"ping": "pong"})
            db.child("ping").child("mouse").update({"ping": "pong"})
            db.child("ping").child("controller").update({"ping": "pong"})
            string = "{time};{x},{y};{hath},{hatv};{circle},{square},{triangle},{dpadx};{heldL},{heldR},{heldD};ID130,{x130},{y130};ID140,{x140},{y140}\n".format(
                x = vis["x"], y = vis["y"],
                hath = hat["x"], hatv = hat["y"],
                square = boolToInt(dpad['square']), triangle = boolToInt(dpad['triangle']),
                dpadx = boolToInt(dpad['x']), circle = boolToInt(dpad['circle']),
                heldL = held['left'], heldR = held['right'], heldD = held['direct'],
                x130 = ID130['x'], y130 = ID130['y'],
                x140=ID140['x'], y140=ID140['y']
            )
            file = open("log.txt", "a+")
            file.write(string)
            file.close()
            t1 = time.time()
            pollrate = db.child('pollrate').get().val()


