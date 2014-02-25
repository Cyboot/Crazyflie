from flight.flightcontroller import FlightController
from flight.connectionmanager import ConnectionManager


global flightcontroller
global connectionmanager

if flightcontroller != None:
    flightcontroller = FlightController()
    connectionmanager = ConnectionManager(flightcontroller)