
from wpilib import IterativeRobot
from wpilib import DigitalOutput
import wpilib
from wpilib.command import Scheduler
from wpilib import LiveWindow

import logging

from oi import OI
from robotMap import RobotMap
from subsystems.driveTrain import DriveTrain
from subsystems.intakeLauncher import IntakeLauncher
from subsystems.portcullis import Portcullis
from commands.autonomous import AutonomousCmd1
from visionState import VisionState

class AresRobot(IterativeRobot):
    def __init__(self):
        super().__init__()
    # IterativeRobot methods
    def robotInit(self):
        # first make logging available (this is instantiated in robotbase)
        self.logger = logging.getLogger('AresRobot')

        # next initialize our RobotMap (defined by wiring)
        self.map = RobotMap()

        # next create standalone objects
        self.visionState = VisionState(self)
        self.lastTime = 0
        self.autonomousCommand = None

        # next initialize subsystems
        try:
            self.info("init drivetrain")
            self.driveTrain = DriveTrain(self)
        except:
            self.error("Problem intializing DriveTrain")

        try:
            self.info("init portcullis")
            self.portcullis = Portcullis(self)
        except:
            self.error("Problem initializing portcullis")

        try:
            self.info("init intake")
            self.intakeLauncher = IntakeLauncher(self)
        except:
            self.error("Problem initializing intakelauncher")

        self.photonicCannon = DigitalOutput(self.map.k_VsPhotonicCannon)

        # last, initialize operator interface
        try:
            self.info("init OI")
            self.oi = OI(self)
        except:
            self.error("Problem initializing OI")
        
        self.info("init done")

    def autonomousInit(self):
        self.info("autonomousInit")
        self.autonomousCommand = AutonomousCmd1(self)
        self.autonomousCommand.start()

    def autonomousPeriodic(self):
        Scheduler.getInstance().run()
        self.updateDashboard()

    def teleopInit(self):
        self.info("teleopInit")
        if self.autonomousCommand:
            self.autonomousCommand.cancel();
            self.autonomousCommand = None
        # we used aimMotor.enableControl here... it should be intrinsic
        # in the running of the default command...

    def teleopPeriodic(self):
        Scheduler.getInstance().run()
        self.updateDashboard()

    def testInit(self):
        self.info("testInit")

    def testPeriodic(self):
        LiveWindow.run()
        self.updateDashboard()

    def disabledInit(self):
        self.info("disabledInit")

    def disabledPeriodic(self):
        Scheduler.getInstance().run()
        self.updateDashboard()

    # logging methods ----------------------------------------
    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    # niscelleany ----------------------------------------------
    def setLight(self, state):
        self.photonicCannon.set(state)

    def updateDashboard(self):
        currentTime = wpilib.Timer.getFPGATimestamp()
        if currentTime - self.lastTime > 1.0:
            self.lastTime = currentTime
            self.driveTrain.updateDashboard()
            self.intakeLauncher.updateDashboard()
            self.portcullis.updateDashboard()

if __name__ == "__main__":
    wpilib.run(AresRobot)
