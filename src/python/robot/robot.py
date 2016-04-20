
import wpilib
import logging

from oi import OI
from robotMap import RobotMap
from subsystems.driveTrain import DriveTrain
from subsystems.intakeLauncher import IntakeLauncher
from subsystems.portcullis import Portcullis

class AresRobot(wpilib.IterativeRobot):

    def robotInit(self):
        # first make logging available (this is instantiated in robotbase)
        self.logger = logging.getLogger('robotpy')

        # next initialize our RobotMap (defined by wiring)
        self.map = RobotMap()

        # next initialize subsystems
        self.driveTrain = DriveTrain(self)
        self.portcullis = Portcullis(self)
        self.intakeLauncher = IntakeLauncher(self)

        # last, initialize operator interface
        self.oi = OI(self)

    def autonomousInit(self):
        pass

    def autonomousPeriodic(self):
        pass

    def teleopInit(self):
        pass

    def teleopPeriodic(self):
        pass

    def testInit(self):
        pass

    def testPeriodic(self):
        pass

    # logging methods ----------------------------------------
    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

if __name__ == "__main__":
    wpilib.run(AresRobot)
