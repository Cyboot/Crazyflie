from cflib.crazyflie.log import LogConfig
class MyLog:
    def __init__(self):
        self.reload()

    def reload(self):
        self._logConfig = LogConfig(name="Magnetometer", period_in_ms=100)
#         self._logConfig.add_variable("stabilizer.roll", "float")
#         self._logConfig.add_variable("stabilizer.pitch", "float")
#         self._logConfig.add_variable("stabilizer.yaw", "float")
#         self._logConfig.add_variable("stabilizer.thrust", "float")

#         self._logConfig.add_variable("pm.vbat", "float")
        
#         self._logConfig.add_variable("motor.m1", "float") #Front (green) 
#         self._logConfig.add_variable("motor.m2", "float") # Right
#         self._logConfig.add_variable("motor.m3", "float") # Back (red)
#         self._logConfig.add_variable("motor.m4", "float") # Left
        
        
    def getLogConfig(self):
        return self._logConfig


    def start(self):
        if self._logConfig.valid:
            # This callback will receive the data
            self._logConfig.data_received_cb.add_callback(self._log_data)
            # This callback will be called on errors
            self._logConfig.error_cb.add_callback(self._log_error)
            # Start the logging
            self._logConfig.start()
        else:
            print "Could not add logconfig since some variables are not in TOC"
            
    def stop(self):
        self._logConfig.stop()
            
    def _log_error(self, logconf, msg):
        """Callback from the log API when an error occurs"""
        print "Error when logging %s: %s" % (logconf.name, msg)

    def _log_data(self, timestamp, data, logconf):
        """Callback froma the log API when data arrives"""
        print "%s: %s" % (logconf.name, data)