# Livestreamer <-> Robot Tracking Suite
This code base contains a number of tracking scripts and a python api for the tracking of livestreamers in order to translate their actions into robot movement.

## Requirements
In order to run the scripts, the following python packages need to be installed before use

### For all scripts
[Pyrebase](https://pypi.org/project/Pyrebase/)

[Requests](https://pypi.org/project/requests/)

[NumPy](https://pypi.org/project/numpy/)

[Pyserial](https://pypi.org/project/pyserial/)

### For vision scripts
These scripts require a webcam and using a PS4 controller

[OpenCV](https://opencv.org/)

[OpenCV Python Bindings](https://pypi.org/project/opencv-python/)

### For controller data
These scripts require using a PS4 controller
[Pygame](https://pypi.org/project/pygame/)


## Setup
Please do the following before using the scripts

### Datebase set up
Before you do anything else, you will want to set up a Google Firebase database. Begin by creating a new project from [here.](https://console.firebase.google.com/u/0/)
[Then, follow those intructions for the **Create a default Storage bucket** section](https://firebase.google.com/docs/storage/web/start).

In addition to those instructions you'll want to do the follow:
1. First you'll need to set up the config file. The config file is structured like so
```{
  "config" : {
        apiKey: '<your-api-key>',
        authDomain: '<your-auth-domain>',
        databaseURL: '<your-database-url>',
        storageBucket: '<your-storage-bucket-url>'
    },

    "firebaseurl": "your-database-url",

    "arduinoport": "/dev/cu.usbmodem146401"
  }
```
Within the above instructions for setting up a firebase, in the section __Add your bucket URL to your app__, there's instructions to generate the firebaseConfig object
```Javascript
var firebaseConfig = {
    apiKey: '<your-api-key>',
    authDomain: '<your-auth-domain>',
    databaseURL: '<your-database-url>',
    storageBucket: '<your-storage-bucket-url>'
  };
```
In the config files replace each element with the corrosponding elements in the firebaseConfig object.
Also replace the firebaseurl with the url shown after databaseURL. The arduinoport can be left as it unless you're using the arduino script which is explained later

2. **Warning: This code base makes unauthenticated calls to this database**
Inside the project, go to Realtime Database section and then to Rules. Change both the read and write sections to true

3. Finally still in the Realtime Database section, go to the Data section and click the triple dots and then __Import Json__,
then upload [base_firebase.json](../main/base_firebase.json).

### Vision Set up
Within this code base there are two vision scripts avaliable, we'll will set up both here
1. First we need to generate calmatrix.txt and caldel.txt where are respectively the calibration matrix and distortion respectively.
These are can be generated using Tiziano Fiorenzani's tutorial, you can ignore the section about setting the raspberry pi.

2. Next you will need to print the aruco markers ([1] and [2]) included in this code base

3. Next you will need to replace [controller.jpg](../main/controller.jpg) with a similar image of your PS4 controller. This works best
when the picture is in similar lightning conditions as you will be using it in and a bright and unusual color is set for the light

4. You will need to play with the camera_number in the config file to find your camera in the OS

### Arduino
The arduino script allows for a controller mod that allows for detecting whether the controller is held in both hands or not as well as option button.
For the purposes of this code base, I'm going to assume if you are attempting this you are familar with arduinos, in which case a circuit diagram and image of how it should look along with the arduino code is provided in the
Arduino-Setup folder. **Importantly you will need to change the arduinoport section of the config file to the port that your arduino is on when connected to your computer**

## Usage
The scripts included are designed to be used through the API provided through [streamerAPI.py](../main/streamerAPI.py).
This API is designed to be used for providing data to a potential robot software to allow it to react and move according to the streamer's actions.
To use it, import streamerAPI,py into your code for manipulating the robot and create an instance of streamertracking.
The functions provided by streamertracking are explained following

### Controller Functions
These functions require a windows computer running the [controllertracking.py script.](../main/controllertracking.py)
They report the status of the first PS4 controller connected to the computer running.

**getJoystick()**
Returns the positions of the controller joysticks in form
```Python
{0:val. 1:val. 2:val, 3:val, 4:0}
```

0 is the X axis of the Left Stick

1 is the Y axis of the Left Stick

2 is the X axis of the Right Stick

3 is the Y axis of the Right Stick

**getDPad()**
Returns the values of the DPad as an X and Y axis pair in form:
```Python
{('x', 0), ('y', 0)}
```

**getButtons()**
Returns the values of the buttons in form:
```Python
{'circle', False), ('square', False), ('triangle', False), ('x', False)
```

### Aruco Vision Function
This function requires a computer running the [visionaruco.py script.](../main/visionaruco.py) and the two aruco markers provided ([1], [2]) printed.

**getAruco()**
Reports the position in camera of the two aruco markers in form
```Python
{'ID130': {'x': 553.0, 'y': 364.0}), 'ID140': {'x': 467.0, 'y': 365.0}
```
### Controller Vision Function
This function requires a computer running the [visioncontroller.py script.](../main/visioncontroller.py) and the controller who's backside was captured during the vision set up.

**getVision()**
Reports the approximate position in camera of the controller shown in controller.jpg in form
```Python
{'x':'648.3563842773438', 'y':'489.273476340554'}
```

### Mouse Function
This function requires a windows computer running the [mousetracking.py script.](../main/mousetracking.py)

**getMouse()**
Reports the last known position of the mouse of the computer running the script in form
```Python
{'x':0, 'y':0}
```
### Arduino Function
This function requires the arduino controller mod described in the Setup section and a computer running the [arduinoreader.py script.](../main/arduinoreader.py)

**getHeldData()**
Reports the state of the buttons of the arduino controller mod in form:
```Python
{'direct':0 , 'left':0, 'right':0}
```
where 0 is not held and 1 is held

### Updating Polling rate
This function changes the rate at this the vision functions, joystick function and mouse function check the database for requests as well as the api checks the database for responses

**updatePollrate(rate)** where rate is the number of seconds in between checks that you want the scripts to make

## Last Notes
For the vision, joystick and mouse functions, the reported values are always approximate both because of the computer vision isn't optimized and there is a delay between the reporting of the values and the  api responding.

Since this system was designed to work distributed over different computers, the vision function and tracking scripts were only tested on OSX, although should work on Windows where as the controller tracking and mouse tracking **only work on Windows**

## References

For Aruco Tracking:

https://www.youtube.com/watch?v=QV1a1G4lL3U

https://www.youtube.com/watch?v=wlT_0fhGrGg

For General Purpose Computer vision tracking:

https://www.youtube.com/watch?v=UquTAf_9dVA

For Mouse tracking:

https://stackoverflow.com/questions/3698635/getting-cursor-position-in-python

For Controller Tracking:

https://gist.github.com/claymcleod/028386b860b75e4f5472

For Python threading:

https://blog.miguelgrinberg.com/post/how-to-make-python-wait

[1]: ../main/aruco-markers/aruco-130.svg
[2]: ../main/aruco-markers/aruco-140.svg