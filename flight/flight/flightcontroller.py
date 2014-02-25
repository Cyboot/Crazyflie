import threading
import time
from controls import gamepad

import logging
logger = logging.getLogger(__name__)

class ConfigValue:
    max = {"throttle":0, "angle":20, "yawrate":180}
    min = {"throttle":20}
    slew = {"rate":30, "limitLow":40, "limitHigh":70}
    trim = {"pitch":0, "roll":0, "yaw":0}

class FlightController(threading.Thread):
    '''
    handling the flightcontrols
    '''
    
    def __init__(self):
        threading.Thread.__init__(self)
        self._cf = None
        self._cm = None
        self._REFRESHRATE = 0.02
        self._gamepad = gamepad
        self._cfg = ConfigValue()
        
        self._roll = 0
        self._pitch = 0
        self._yawrate = 0
        self._throttle = 0
        self._thrust = 0
        
    def setConnectionManager(self, cm):
        self._cm = cm
        
    def setCrazyflie(self, cf):
        self._cf = cf

    def _sendValues(self):
        self._cf.commander.send_setpoint(self._roll, self._pitch, self._yawrate, self._thrust)
        
    def _updateThrust(self):
        ''' calculate the Throttle/Thrust with SLEW support  '''
        oldThrottle = self._throttle
        throttleRaw = -float(gamepad.axisLeft_Y)  # @UndefinedVariable
        if throttleRaw <= 0:
            self._throttle = 0
        else:
            min = self._cfg.min["throttle"]  # @ReservedAssignment
            max = self._cfg.max["throttle"]  # @ReservedAssignment
            self._throttle = (throttleRaw * (max - min) + min)
            
        maxDeltaThrottle = self._cfg.slew["rate"] * self._REFRESHRATE
        
        # slewrate
        if self._throttle < -10:
            self._throttle = 0
        elif self._throttle < 0:
            pass
        elif oldThrottle > self._cfg.slew["limitLow"] and self._throttle < oldThrottle - maxDeltaThrottle:
            if oldThrottle > self._cfg.slew["limitHigh"]:
                self._throttle = self._cfg.slew["limitHigh"]
            else:
                self._throttle = oldThrottle - maxDeltaThrottle
    
        if self._throttle < self._cfg.min["throttle"]:
            self._throttle = 0
            
        # convert throttle (in %) to thrust (in rpm)
        MINTHRUST = 10001 
        MAXTHRUST = 60000       
        self._thrust = ((MAXTHRUST - MINTHRUST) * self._throttle / 100.) + MINTHRUST - 10
        
    
    def _updateValues(self):
        ''' updates the pitch and roll axis'''
        self._pitch = -gamepad.axisRight_Y / 100. * self._cfg.max["angle"] + self._cfg.trim["pitch"]  # @UndefinedVariable
        self._roll = gamepad.axisRight_X / 100. * self._cfg.max["angle"] + self._cfg.trim["roll"]  # @UndefinedVariable
        self._yawrate = gamepad.axisLeft_X / 100. * self._cfg.max["yawrate"] + self._cfg.trim["yaw"]  # @UndefinedVariable
    
    
    def _run(self):
        while True:
            time.sleep(self._REFRESHRATE)
            
            self._updateThrust()
            self._updateValues()
            logger.debug("%.2f - %.2f - %.2f  @  %ik", self._pitch, self._roll, self._yawrate, (self._thrust / 100))
            if self._cm.isConnected():
                self._sendValues()
            
