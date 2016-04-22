
from wpilib.command import Subsystem
from wpilib import SmartDashboard

class IntakeLauncher(Subsystem):

    def __init__(self, robot, name=None):
        super().__init__(name=name)
        self.robot = robot

    def updateDashboard(self):
        pass
