from networktables import NetworkTable
from wpilib import SmartDashboard

class VisionState:
    """A class to encapsulate state received from remote vision server"""
    k_TableName = "Vision"
    def __init__(self, robot):
        self.robot = robot
        self.table = SmartDashboard.getTable().getSubTable(self.k_TableName)

        # controlled via driverstation
        self.AutoAimEnabled = False
        self.TargetHigh = True

        # controlled via remote vision server
        self.FPS = 0
        self.TargetAcquired = False
        self.TargetX = 0
        self.TargetY = 0

        # our listener is "bound" to self, called when we receive notifications
        # from the vision server.
        def _listener(table, key, value, isNew):
            if key == "AutoAimEnabled":
                self.AutoAimEnabled = value
            elif key == "FPS":
                self.FPS = value
            elif key == "TargetAcquired":
                self.TargetAcquired = value
            elif key == "TargetX":
                self.TargetX = value
            elif key == "TargetY":
                self.TargetY = value
            elif key == "~TYPE~":
                pass
            else:
                self.robot.warning("Unexpected Vision key: "+key)

        self.table.addTableListener(_listener)

    def toggleAimState(self, toggleEnable, toggleTarget):
        if targetEnable:
            self.AutoAimEnabled = not self.AutoAimEnabled
            self.table.putBoolean("AutoAimEnabled", self.AutoAimEnabled)
            self.robot.setLight(self.AutoAimEnabled)

        if toggleTarget:
            self.TargetHigh = not self.TargetHigh

        DriveLockedOnTarget = False
        LauncherLockedOnTarget = False

    def getTargetHeading(self, currentHeading):
        return self.TargetX + currentHeading

    def getTargetElevation(self, currentElevation):
        return self.TargetY + currentElevation

    def wantsControl(self):
        return self.AutoAimEnabled
