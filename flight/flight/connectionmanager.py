import threading
from cflib.crazyflie import Crazyflie
import time
import cflib.crtp

import logging
logger = logging.getLogger(__name__)

class ConnectionManager(threading.Thread):
    '''
    handling all connection with and from crazyflie
    '''

    def __init__(self, flightcontroller):
        self._flightcontroller = flightcontroller
        
        # Crazyflie obj + callbacks
        self._cf = Crazyflie()
        self._cf.connected.add_callback(self._connected)
        self._cf.disconnected.add_callback(self._disconnected)
        self._cf.connection_failed.add_callback(self._connection_failed)
        self._cf.connection_lost.add_callback(self._connection_lost)
        
        self._isConnected = False
        
        self._flightcontroller.setConnectionManager(self)
        self._flightcontroller.setCrazyflie(self._cf)
        
        
        
    def _connection_failed(self, link_uri, msg):
        logger.debug("Connection to %s failed: %s" % (link_uri, msg))
        self._isConnected = False
        self._link = None

    def _connection_lost(self, link_uri, msg):
        logger.debug("Connection to %s lost: %s" % (link_uri, msg))
        self._isConnected = False
        self._link = None

    def _disconnected(self, link_uri):
        logger.info("Disconnected from %s" % link_uri)
        self._isConnected = False
        self._link = None
    
    def _connected(self, link_uri):
        logger.debug("Connected to %s" % link_uri)
        self._isConnected = True
        

    def _reconnect(self):
        logger.info("Scanning for Crazyflies...")
        crazyfliesFound = cflib.crtp.scan_interfaces()
    
        if crazyfliesFound:
            for i in crazyfliesFound:
                self._link = i[0]
                logger.info("Found: %s" % self._link)
                self._cf.open_link(self._link)
                break
        else:
            logger.info("No Crazyflies found")
    
    
    def _run(self):
        while True:
            if self._isConnected == False:
                self._reconnect()
                time.sleep(3)
            
            time.sleep(0.5)