#adapted from https://gist.github.com/claymcleod/028386b860b75e4f5472
import pygame
import requests
import time
import json
from pathlib import Path




class PS4Controller(object):
    """Class representing the PS4 controller. Pretty straightforward functionality."""

    controller = None
    axis_data = {1:0, 2:0, 3:0, 4:0}
    button_data = None
    hat_data = None


    def init(self):
        """Initialize the joystick components"""

        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()

    def listen(self):
        cwd = Path.cwd()
        configfile = cwd / "config.json"

        with open(configfile) as f:
            data = json.load(f)

        firebase = data['firebaseurl']

        pollrate = requests.get("{url}pollrate.json".format(url=firebase)).json()

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


        t1 = time.time()
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
                requests.patch('{url}controldpad.json'.format(url = firebase),
                               json={"square": d[0], "x": d[1], "circle": d[2], "triangle": d[3]})
                prevd = (d[0], d[1], d[2], d[3])

            left = self.button_data[13]
            right = self.button_data[14]
            up = self.button_data[11]
            down = self.button_data[12]
            hath = 0
            if left:
                hath = -1
            elif right:
                hath = 1
            hatv = 0
            if up:
                hatv = 1
            elif down:
                hatv = -1
            if hath != prevhat[0] or hatv != prevhat[1]:
                requests.patch('{url}controlhat.json'.format(url = firebase),
                               json={"x": hath, "y": hatv})
                prevhat = (hath, hatv)

            if time.time() - t1 >= pollrate:
                ping = requests.get(
                    "{url}ping/controller/ping.json".format(url = firebase))
                if ping.json() == "pong":
                    requests.patch(
                        '{url}joystick.json'.format(url = firebase),
                        json=self.axis_data)
                    requests.patch(
                        '{url}ping/controller.json'.format(url = firebase),
                        json={'ping': 'ping'})
                t1 = time.time()
                pollrate = requests.get(
                    "{url}pollrate.json".format(url=firebase)).json()


                # print(self.button_data)
                # print(self.axis_data)
                # print(self.hat_data)


if __name__ == "__main__":
    ps4 = PS4Controller()
    ps4.init()
    ps4.listen()
