from cflib.crazyflie.log import LogConfig
class MyLog:
    def __init__(self):
        self.reload()

    def reload(self):
        self._lc_stab = LogConfig(name="Magnetometer", period_in_ms=100)
#         self._lc_stab.add_variable("stabilizer.roll", "float")
#         self._lc_stab.add_variable("stabilizer.pitch", "float")
#         self._lc_stab.add_variable("stabilizer.yaw", "float")
#         self._lc_stab.add_variable("stabilizer.thrust", "float")

#         self._lc_stab.add_variable("pm.vbat", "float")
        
#         self._lc_stab.add_variable("motor.m1", "float") #Front (green) 
#         self._lc_stab.add_variable("motor.m2", "float") # Right
#         self._lc_stab.add_variable("motor.m3", "float") # Back (red)
#         self._lc_stab.add_variable("motor.m4", "float") # Left
        
        
    def getLogConfig(self):
        return self._lc_stab


    def start(self):
        if self._lc_stab.valid:
            # This callback will receive the data
            self._lc_stab.data_received_cb.add_callback(self._log_data)
            # This callback will be called on errors
            self._lc_stab.error_cb.add_callback(self._log_error)
            # Start the logging
            self._lc_stab.start()
        else:
            print "Could not add logconfig since some variables are not in TOC"
            
    def stop(self):
        self._lc_stab.stop()
            
    def _log_error(self, logconf, msg):
        """Callback from the log API when an error occurs"""
        print "Error when logging %s: %s" % (logconf.name, msg)

    def _log_data(self, timestamp, data, logconf):
        """Callback froma the log API when data arrives"""
        print "%s: %s" % (logconf.name, data)