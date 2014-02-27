import logging

from controls import sixaxis
from controls.driver import PyGameDriver
from controls.driver import SixAxisDriver
from controls.gamepad import Gamepad


logging.basicConfig(level=logging.INFO,format='%(levelname)-5s- %(name)-15s  >>  %(message)s')
logger = logging.getLogger(__name__)
# handler = logging.StreamHandler()
# formatter = logging.Formatter('%(levelname)-5s - %(name)-12s : %(message)s')
# handler.setFormatter(formatter)
# logger.addHandler(handler)

#variables
gamepad = Gamepad()
_driver = None

def start():
    try:
        if _checkForSixaxis():
            logger.info("starting controller with SIXAXIS driver")
            _driver = SixAxisDriver(gamepad)
        else:
            logger.info("starting controller with PYGAME driver")
            _driver = PyGameDriver(gamepad)
            
        _driver.start()
    except:
        logger.error("Error initializing driver")
    
def isPressed(keycombination):
    return keycombination.isPressed(gamepad)
    

def _checkForSixaxis():
    """ check if sixaxis is available (default for linux)"""
    return sixaxis.init("/dev/input/js1")
