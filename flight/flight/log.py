from cflib.crazyflie.log import LogConfig

import logging
logger = logging.getLogger(__name__)

class CFStatus:
    def __init__(self):
        self.motor_1 = 0
        self.motor_2 = 0
        self.motor_3 = 0
        self.motor_4 = 0
    
        self.pitch = 0
        self.roll = 0
        self.yaw = 0
        self.thrust = 0
    
        self.bat = 0
    
    def __str__(self):
        bat = "bat: %0.2f, " % self.bat
        stab = "pitch: %.1f, roll: %.1f, yaw: %.1f, trust: %.1f " % (self.pitch, self.roll, self.yaw, self.thrust)
        motor = "m1: %i, m2: %i, m3: %i, m4: %i" % (self.motor_1, self.motor_2, self.motor_3, self.motor_4)
        
        return bat + stab + motor
        
        
class CFLog():
    
    def __init__(self):
        self.status = CFStatus()

    def start(self, cf):
        self._lc_stab = LogConfig(name="Log-Stab", period_in_ms=50)
        self._lc_stab.add_variable("stabilizer.roll", "float")
        self._lc_stab.add_variable("stabilizer.pitch", "float")
        self._lc_stab.add_variable("stabilizer.yaw", "float")
        self._lc_stab.add_variable("stabilizer.thrust", "float")
        
        self._lc_motor = LogConfig(name="Log-Motor", period_in_ms=50)
        self._lc_motor.add_variable("pm.vbat", "float")
        self._lc_motor.add_variable("motor.m1", "float")  # Front (green) 
        self._lc_motor.add_variable("motor.m2", "float")  # Right
        self._lc_motor.add_variable("motor.m3", "float")  # Back (red)
        self._lc_motor.add_variable("motor.m4", "float")  # Left

        cf.log.add_config(self._lc_stab)
        cf.log.add_config(self._lc_motor)
        if self._lc_stab.valid and self._lc_motor.valid:
            self._lc_stab.data_received_cb.add_callback(self._log_data)
            self._lc_stab.error_cb.add_callback(self._log_error)
            self._lc_stab.start()
            self._lc_motor.data_received_cb.add_callback(self._log_data)
            self._lc_motor.error_cb.add_callback(self._log_error)
            self._lc_motor.start()
            logger.info("Starting CFLog")
        else:
            logger.error("Could not add logconfig since some variables are not in TOC")
            
    def stop(self):
        self._lc_stab.stop()
            
    def _log_error(self, logconf, msg):
        """Callback from the log API when an error occurs"""
        logger.info("Error when logging %s: %s" % (logconf.name, msg))

    def _log_data(self, timestamp, data, logconf):
        """Callback froma the log API when data arrives"""
        if logconf.name == "Log-Stab":
            self.status.pitch = data["stabilizer.pitch"]
            self.status.roll = data["stabilizer.roll"]
            self.status.yaw = data["stabilizer.yaw"]
            self.status.thrust = data["stabilizer.thrust"]
        else:
            self.status.bat = data["pm.vbat"]    
            self.status.motor_1 = data["motor.m1"]    
            self.status.motor_2 = data["motor.m2"]    
            self.status.motor_3 = data["motor.m3"]    
            self.status.motor_4 = data["motor.m4"]    
        
        logger.info("%s" % self.status)
#         logger.info("%s: %s" % (logconf.name, data))
