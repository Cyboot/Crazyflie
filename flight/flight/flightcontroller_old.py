import time
from func import getLink, init, getThrust, getPitch, getRoll, getYawrate, var
from cflib.crazyflie import Crazyflie
from threading import Thread
from sixaxis import isRunning
from log import MyLog

class FlightController:
    def __init__(self):
        # Crazyflie obj + callbacks
        self._cf = Crazyflie()
        self._cf.connected.add_callback(self._connected)
        self._cf.disconnected.add_callback(self._disconnected)
        self._cf.connection_failed.add_callback(self._connection_failed)
        self._cf.connection_lost.add_callback(self._connection_lost)
        
        self._myLog = MyLog()
        self._isConnected = False
        Thread(target=self._run).start()
        
    def reconnect(self):
        link = getLink()
        if link != False:
            self._cf.open_link(link)  # connect to crazyflie
    
    def _connection_failed(self, link_uri, msg):
        print "Connection to %s failed: %s" % (link_uri, msg)
        self._isConnected = False

    def _connection_lost(self, link_uri, msg):
        print "Connection to %s lost: %s" % (link_uri, msg)
        self._isConnected = False

    def _disconnected(self, link_uri):
        print "Disconnected from %s" % link_uri
        self._isConnected = False
        self._myLog.stop()
    
    def _connected(self, link):
        self._isConnected = True
        
        # add log
#         self._cf.log.add_config(self._myLog.getLogConfig())
#         self._myLog.start()

    def _run(self):
        """ the active Thread """
        self._cf.commander.send_setpoint(0, 0, 0, 15000)
        time.sleep(0.2)
        while isRunning():# and self._isConnected:
            thrust = getThrust()
            pitch = getPitch()
            roll = getRoll()
            yawrate = getYawrate()
            self._cf.commander.send_setpoint(roll, pitch, yawrate, thrust)
            time.sleep(0.02)
            print pitch, " - ", roll, " - ",yawrate," @ ",thrust,"   || ",var.trim["pitch"]," ",var.trim["roll"]," ",var.trim["yaw"]
        
            if self._isConnected == False:
                print "trying to reconnect... "
                self.reconnect()
                time.sleep(5)
        
        self._cf.commander.send_setpoint(0, 0, 0, 0)
        time.sleep(0.01)
        self._cf.close_link()
        

init()
global flightcontroller
flightcontroller = FlightController()
