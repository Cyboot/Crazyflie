import threading
import time
from controls import gamepad

import logging
logger = logging.getLogger(__name__)

class ConfigValue:
    max = {"throttle":80, "angle":20, "yawrate":180}
    min = {"throttle":30}
    slew = {"rate":30, "limitLow":40, "limitHigh":70}
    trim = {"pitch":0, "roll":0, "yaw":0}

class FlightController(threading.Thread):
    '''
    handling the flightcontrols
    '''
    
    def __init__(self):
        threading.Thread.__init__(self)
        self.setDaemon(False)
        
        self._cf = None
        self._cm = None
        self._REFRESHRATE = 0.03
        self._gamepad = gamepad
        self._cfg = ConfigValue()
        
        self.roll = 0
        self.pitch = 0
        self.yawrate = 0
        self.throttle = 0
        self.thrust = 0
        
    def setConnectionManager(self, cm):
        self._cm = cm
        
    def setCrazyflie(self, cf):
        self._cf = cf

    def _sendValues(self):
        self._cf.commander.send_setpoint(self.roll, self.pitch, self.yawrate, self.thrust)
        
    def _updateThrust(self):
        ''' calculate the Throttle/Thrust with SLEW support  '''
        oldThrottle = self.throttle
        throttleRaw = -float(gamepad.axisLeft_Y)  # @UndefinedVariable
        if throttleRaw <= 0:
            self.throttle = 0
        else:
            min = self._cfg.min["throttle"]  # @ReservedAssignment
            max = self._cfg.max["throttle"]  # @ReservedAssignment
            self.throttle = (throttleRaw/100. * (max - min) + min)
            
        maxDeltaThrottle = self._cfg.slew["rate"] * self._REFRESHRATE
        
        # slewrate
        if throttleRaw < -10:
            self.throttle = 0
        elif throttleRaw < 0:
            pass
        elif oldThrottle > self._cfg.slew["limitLow"] and self.throttle < oldThrottle - maxDeltaThrottle:
            if oldThrottle > self._cfg.slew["limitHigh"]:
                self.throttle = self._cfg.slew["limitHigh"]
            else:
                self.throttle = oldThrottle - maxDeltaThrottle
    
        if self.throttle < self._cfg.min["throttle"]:
            self.throttle = 0
            
        # convert throttle (in %) to thrust (in rpm)
        MINTHRUST = 10001 
        MAXTHRUST = 60000       
        self.thrust = ((MAXTHRUST - MINTHRUST) * self.throttle / 100.) + MINTHRUST - 10
        
    
    def _updateValues(self):
        ''' updates the pitch and roll axis'''
        self.pitch = -gamepad.axisRight_Y / 100. * self._cfg.max["angle"] + self._cfg.trim["pitch"]  # @UndefinedVariable
        self.roll = gamepad.axisRight_X / 100. * self._cfg.max["angle"] + self._cfg.trim["roll"]  # @UndefinedVariable
        self.yawrate = gamepad.axisLeft_X / 100. * self._cfg.max["yawrate"] + self._cfg.trim["yaw"]  # @UndefinedVariable
    
        if gamepad.buttons["R1"]:  # @UndefinedVariable
            self.pitch = 360
        elif gamepad.buttons["R2"]:  # @UndefinedVariable
            self.pitch = -360
    
    def run(self):
        while True:
            time.sleep(self._REFRESHRATE)
            
            self._updateThrust()
            self._updateValues()
#             logger.info("%2.1f - %2.1f - %2.1f  @  %.1fk", self.pitch, self.roll, self.yawrate, (self.thrust / 1000.))
            if self._cm.isConnected:
                self._sendValues()
            
