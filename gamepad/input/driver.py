import threading
import time
import pygame
import sixaxis

import logging
logger = logging.getLogger(__name__)

class PyGameDriver(threading.Thread):
    '''
    updates the gamepad class
    '''

    def __init__(self, gamepad):
        threading.Thread.__init__(self)
        self._REFRESH_RATE = 0.1
        self._gamepad = gamepad
        
        pygame.init()
        if pygame.joystick.get_count() < 1:
            logger.warn("no joystick/gamepad found, abort")
            raise Exception("no joystick/gamepad found") 
        
        self._joystick = pygame.joystick.Joystick(0)
        self._joystick.init()
        logger.info('Initialized Joystick : %s' % self._joystick.get_name())
        
    
    def run(self):
        while True:
            self._update()
            time.sleep(self._REFRESH_RATE)

            # DEBUG: print Gamepad           
#             print self._gamepad
    
    
    def _update(self):
        pygame.event.pump()
        
        # Buttons
        self._gamepad.buttons["square"] = self._joystick.get_button(0)
        self._gamepad.buttons["cross"] = self._joystick.get_button(1)
        self._gamepad.buttons["circle"] = self._joystick.get_button(2)
        self._gamepad.buttons["triangle"] = self._joystick.get_button(3)
        
        self._gamepad.buttons["R1"] = self._joystick.get_button(4)
        self._gamepad.buttons["L1"] = self._joystick.get_button(5)
        self._gamepad.buttons["R2"] = self._joystick.get_button(6)
        self._gamepad.buttons["L2"] = self._joystick.get_button(7)
        
        self._gamepad.buttons["select"] = self._joystick.get_button(8)
        self._gamepad.buttons["start"] = self._joystick.get_button(9)
        self._gamepad.buttons["ps3"] = self._joystick.get_button(12)
        
        # Hat (left digital pad)
        hat = self._joystick.get_hat(0)
        self._gamepad.buttons["left"] = hat[0] == -1
        self._gamepad.buttons["right"] = hat[0] == 1
        self._gamepad.buttons["up"] = hat[1] == 1
        self._gamepad.buttons["down"] = hat[1] == -1

        # Axis    
        self._gamepad.axisLeft_X = self._joystick.get_axis(0)
        self._gamepad.axisLeft_Y = self._joystick.get_axis(1)
        self._gamepad.axisRight_X = self._joystick.get_axis(2)
        self._gamepad.axisRight_Y = self._joystick.get_axis(3)
    
        
class SixAxisDriver(threading.Thread):
    '''
    updates the gamepad class
    '''

    def __init__(self, gamepad):
        threading.Thread.__init__(self)
        self._REFRESH_RATE = 0.1
        self._gamepad = gamepad
        
        # should not be necassary because it is already inited from __init__.checkForSixaxis()
        # sixaxis.init("/dev/input/js1")
        
    
    def run(self):
        while True:
            self._update()
            time.sleep(self._REFRESH_RATE)

            # DEBUG print Gamepad            
            print self._gamepad
    
    def _update(self):
        state = sixaxis.get_state()
        
        # Buttons
        self._gamepad.buttons["square"] = state["square"]
        self._gamepad.buttons["cross"] = state["square"]
        self._gamepad.buttons["circle"] = state["square"]
        self._gamepad.buttons["triangle"] = state["square"]
        self._gamepad.buttons["R1"] = state["trig0"]
        self._gamepad.buttons["L1"] = state["trig1"]
        self._gamepad.buttons["R2"] = state["trig2"]
        self._gamepad.buttons["L2"] = state["trig3"]
        self._gamepad.buttons["select"] = state["select"]
        self._gamepad.buttons["start"] = state["start"]
        self._gamepad.buttons["ps3"] = state["ps"]
        self._gamepad.buttons["left"] = state["bottomleft"]
        self._gamepad.buttons["right"] = state["bottomright"]
        self._gamepad.buttons["up"] = state["bottomup"]
        self._gamepad.buttons["down"] = state["bottomdown"]
        
        # Axis
        self._gamepad.axisLeft_X = state["leftx"] / 100.
        self._gamepad.axisLeft_Y = state["lefty"] / 100.
        self._gamepad.axisRight_X = state["rightx"] / 100.
        self._gamepad.axisRight_Y = state["righty"] / 100.
