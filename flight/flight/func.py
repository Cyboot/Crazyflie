#!/usr/bin/python
# -*- coding: latin-1 -*-

from cflib.crtp import init_drivers, scan_interfaces
import logging
import controls.sixaxis
from threading import Thread
import time
from controls.sixaxis import joy, shutdown

###### global variable ######
class Var:
    def __init__(self):
        self.max = {"throttle":0, "angle":0, "yawrate":0}
        self.min = {"throttle":20}
        
        self.slew = {"rate":30, "limitLow":40, "limitHigh":70}
        
        self.trim = {"pitch":0, "roll":0, "yaw":0}
        
global var
var = Var()
#############################

def init():
    logging.basicConfig(level=logging.WARNING)
    # init drivers
    init_drivers(enable_debug_driver=False)
    
    # intit & start Controllerinput-Thread
    GamepadController()
    

def reloadConfig():
    """ reload the config files """
    print "---===  load cfg  ===---"
    cfgFile = open("../cfg/config.cfg", "r")
    lines = cfgFile.readlines()
    
    for l in lines:
        l = l.replace("\n", "")
        if (l.count("#") and l.index("#") == 0) or l.count(":") == 0:
            continue
        tmp = l.split(":")
        tmp[0] = tmp[0].replace("trim", "")
        tmp[0] = tmp[0].replace("max", "")
        tmp[0] = tmp[0].replace("slew", "")
        tmp[0] = tmp[0].replace("min", "")
        
        if tmp[0] in var.min:
            var.min[tmp[0]] = float(tmp[1])
            print tmp[0], " = ", tmp[1]
        if tmp[0] in var.trim:
            var.trim[tmp[0]] = int(tmp[1])
            print tmp[0], " = ", tmp[1]
        if tmp[0] in var.max:
            var.max[tmp[0]] = int(tmp[1])
            print tmp[0], " = ", tmp[1]
        if tmp[0] in var.slew:
            var.slew[tmp[0]] = int(tmp[1])
            print tmp[0], " = ", tmp[1]
        
    print "---=== loaded cfg ===---"
    
    

def getLink():
    print "Scanning for Crazyflies..."
    crazyfliesFound = scan_interfaces()
    
    if crazyfliesFound:
        for i in crazyfliesFound:
            print "Found: ", i[0]
            return i[0]
    else:
        print "No Crazyfly found"
        return False
        
def getThrust():
    MINTHRUST = 10001 
    MAXTHRUST = 60000
    resultThrottle = throttle #* (var.max["throttle"] / 100.)
    return ((MAXTHRUST - MINTHRUST) * resultThrottle / 100) + MINTHRUST - 10

def getPitch():
    return (pitch / 100. * var.max["angle"]) + var.trim["pitch"]

def getRoll():
    return (roll / 100. * var.max["angle"]) + var.trim["roll"]

def getYawrate():
    return (yawrate / 100. * var.max["yawrate"]) + var.trim["yaw"]

class GamepadController:
    def __init__(self):
        Thread(target=self._run).start()
    
    def _run(self):
        controls.sixaxis.init("/dev/input/js0")
        reloadConfig()
        
        global throttle
        global pitch
        global roll
        global yawrate
        global flightcontroller
        
        throttle = 0
        delta = 0.1
        try:
            while controls.sixaxis.isRunning():
                # calc throttle
                oldThrottle = throttle
                
                joyPercent = -float(joy["lefty"])/100
                if joyPercent == 0:
                    throttle = 0
                else:
                    throttle = (joyPercent * (80-20)) + var.min["throttle"]
#                 print "joy: ",joyPercent," - ",throttle

                maxDeltaThrottle = var.slew["rate"] * delta
                
                # slewrate
                if throttle < -10:
                    throttle = 0
                elif throttle < 0:
                    pass
                elif oldThrottle > var.slew["limitLow"] and throttle < oldThrottle - maxDeltaThrottle:
                    if oldThrottle > var.slew["limitHigh"]:
                        throttle = var.slew["limitHigh"]
                    else:
                        throttle = oldThrottle - maxDeltaThrottle
                        
                if throttle < var.min["throttle"]:
                    throttle = 0
                    
                
                pitch = -joy["righty"]
                roll = joy["rightx"]
                yawrate = joy["leftx"]
    
                if joy["start"] == True:
                    raise(KeyboardInterrupt)
                if joy["PS3"] == True:
                    reloadConfig()
                    
                time.sleep(delta)
        except KeyboardInterrupt:
            print "Press any Controller Button to exit"
            shutdown()
            
