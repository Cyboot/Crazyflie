from flight.flightcontroller import FlightController
from flight.connectionmanager import ConnectionManager
import cflib.crtp
from flight.log import CFLog


def init():
    # driver
    cflib.crtp.init_drivers(enable_debug_driver=False)
    
    global flightCtrl
    global conMng
    flightCtrl = FlightController()
    conMng = ConnectionManager(flightCtrl)
    
    flightCtrl.start()
    conMng.start()
    
def getCFStatus():
    return conMng.cfLog.status

def getFlightController():
    return flightCtrl