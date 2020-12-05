import requests
import pygame
import pyrebase

class PS4Controller(object):
    """Class representing the PS4 controller. Pretty straightforward functionality."""

    controller = None
    axis_data = None
    button_data = None
    hat_data = None

    config = {
        "apiKey": "AIzaSyCfSSnLmj5KcoD6B4fgsgbiSsj_x3-o9Bc",
        "authDomain": "hri-bottuber.firebaseapp.com",
        "databaseURL": "https://hri-bottuber.firebaseio.com",
        "storageBucket": "hri-bottuber.appspot.com"
    }

    firebase = pyrebase.initialize_app(config)

    db = firebase.database()


    def init(self):
        """Initialize the joystick components"""

        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()

    def listen(self):
        """Listen for events to happen"""
        prevhat = (0, 0)
        prevd = (False, False, False, False)
        if not self.axis_data:
            self.axis_data = {}

        if not self.button_data:
            self.button_data = {}
            for i in range(self.controller.get_numbuttons()):
                self.button_data[i] = False

        if not self.hat_data:
            self.hat_data = {}
            for i in range(self.controller.get_numhats()):
                self.hat_data[i] = (0, 0)

        while True:

            for event in pygame.event.get():
                if event.type == pygame.JOYAXISMOTION:
                    self.axis_data[event.axis] = round(event.value, 2)
                    print(self.axis_data)
                elif event.type == pygame.JOYBUTTONDOWN:
                    self.button_data[event.button] = True
                elif event.type == pygame.JOYBUTTONUP:
                    self.button_data[event.button] = False
                elif event.type == pygame.JOYHATMOTION:
                    self.hat_data[event.hat] = event.value

                # Insert your code on what you would like to happen for each event here!
                # In the current setup, I have the state simply printing out to the screen.
            d = (self.button_data[0], self.button_data[1], self.button_data[2], self.button_data[3])
            if (d[0] !=  prevd[0]) or (d[1] !=  prevd[1]) or (d[2] !=  prevd[2]) or (d[3] !=  prevd[3]):
                data = self.db.child("controldpad").update(
                    {"square": d[0], "x": d[1], "circle": d[2], "triangle": d[3]})
                prevd = (d[0], d[1], d[2], d[3])
            if self.hat_data[0][0] != prevhat[0] or self.hat_data[0][1] != prevhat[1]:
                data = self.db.child("controlhat").update(
                    {"x": self.hat_data[0][0], "y": self.hat_data[0][1]})
                prevhat = (self.hat_data[0][0], self.hat_data[0][1])

                # print(self.button_data)
                # print(self.axis_data)
                # print(self.hat_data)


if __name__ == "__main__":
    ps4 = PS4Controller()
    ps4.init()
    ps4.listen()