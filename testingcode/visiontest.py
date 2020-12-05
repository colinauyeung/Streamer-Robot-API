import numpy as np
import cv2
import pyrebase
import time

boundary = ([86, 31, 4], [220, 88, 50])
cap = cv2.VideoCapture(0)

tracker = cv2.TrackerCSRT_create()
ret, frame = cap.read()

bbox = cv2.selectROI("Tracking", frame, False)
tracker.init(frame, bbox)

firebase = pyrebase.initialize_app(config)

db = firebase.database()

t1 = time.time()
def drawBox(img, bbox):
    x,y,w,h = bbox
    cv2.rectangle(img, (int(x), int(y)), (int(x+w), int(y+h)), (255, 0, 255), 3, 1)

while(True):
    timer = cv2.getTickCount()
    # Capture frame-by-frame
    ret, frame = cap.read()

    success,bbox = tracker.update(frame)


    if success :
        drawBox(frame, bbox)
    else:
        cv2.putText(frame, "Lost", (75, 75), cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (0, 0, 255), 2)

    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
    cv2.putText(frame, str(int(fps)), (75,50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
    # Our operations on the frame come here
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    hue, saturation, value = cv2.split(hsv)
    # cv2.imshow('Saturation Image', saturation)

    lower = np.array(boundary[0], dtype="uint8")
    upper = np.array(boundary[1], dtype="uint8")
    # find the colors within the specified boundaries and apply
    # the mask
    mask = cv2.inRange(frame, lower, upper)
    output = cv2.bitwise_and(frame, frame, mask=mask)
    # show the images
    # cv2.imshow("images", np.hstack([frame, output]))

    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if time.time() - t1 >= 5:
        print({"x":str(bbox[0]), "y":str(bbox[1])})
        ping = db.child("ping").child("ping").get()
        if ping.val() == "pong":
            data = db.child("controlvis").update({"x":str(bbox[0]), "y":str(bbox[1])})
            db.child("ping").update({"ping": "ping"})
            t1 = time.time()


# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()