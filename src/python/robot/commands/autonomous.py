

from wpilib.command import CommandGroup

import commands.driveTrainCmds as DTCmds
import commands.intakeLauncherCmds as ILCmds
import commands.visionCmds as VCmds
from oi import OI

class AutonomousCmd1(CommandGroup):

    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        self.barrierType = robot.oi.barrierType.getSelected()
        self.strategy = robot.oi.strategy.getSelected()
        self.position = robot.oi.startingFieldPosition.getSelected()

        if self.strategy == OI.k_NoMoveStrategy:
            self.addSequential(DTCmds.AutoNoDrive(self.robot))
        else:
            if self.robot.intakeLauncher:
                self.addSequential(ILCmds.LauncherGoToNeutralCommand(), 3)

            if self.robot.porcullis:
                if self.getPorcullisBeginDown():
                    self.addSequential(PCCmds.MoveDown(), 2)
                else:
                    self.addSequential(PCCmds.MoveUp(), 2)

            distance = self.getTraveDistance()
            speed = self.getSpeed()
            turnAngle = self.getTurnAngle()

            if self.strategy == OI.k_CrossStrategy:
                slef.addSequential(DTCmds.AutoDriveStraight(distances, speed))
            elif self.strategy == OI.k_CrossBlindShotStrategy:
                self.addSequential(DTCmds.AutoDriveStraight(distance, speed))
                self.addSequential(DTCmds.AutoRotateDegrees(turnAngle))
                # incomplete...
            elif self.strategy == OI.k_CrossVisionShotStrategy:
                self.addSequential(DTCmds.AutoDriveStraight(distance, speed))
                self.addSequential(DTCmds.AutoRotateDegrees(turnAngle))
                self.addSequential(VCmds.AutoAimControl(True, True))
                self.addSequential(VCmds.DriveAndAim())
                self.addSequential(ILCmds.AutoLaunchCommand())
            else:
                self.robot.error("Unimplemented auto strategy " + self.strategy)

    def end(self):
        self.robot.info("AutoCommand1 end")
        super().end()

    def interrupted(self):
        self.robot.info("AutoCommand1 interrupted")
        super().interrupted()
        self.end()

    def getPortcullisBeginDown(self):
        if self.barrierType == OI.k_LowBarBarrier:
            return True
        elif self.barrierType == OI.k_PortcullisBarrier:
            return True
        else:
            return False

    def getTravelDistance(self):
        """ returns the combined distance associated with field position
        and barrier type
        """

        # barrierDist differs for each barrier type
        barrierDist = {
                        OI.k_LowBarBarrier: 130,
                        OI.k_MoatBarrier: 145,
                        OI.k_RoughTerrainBarrier: 180,
                        OI.k_RockWallBarrier: 150,
                        OI.k_PortcullisBarrier: 140,
                        OI.k_RampartsBarrier: 150
                        } [self.barrierType]

        # positionDistance is distance after barrier cross for shooting
        # numbers are courtesy Andalucia
        positionDist = {
                        1: 38.,
                        2: 101.05,
                        3: 74.1,
                        4: 75.09,
                        5: 104.97,
                        } [self.position]

        return barrierDist + positionDist

    def getSpeed(self):
        """ returns the speed required to cross the selected barrier.
        Note that this can be positive or negative. Negative speeds presume
        that the robot has been position backward on the field.
        Also note that speed assume driveTrain is operating in velocity mode.
        """
        barrierSpeed = {
                        OI.k_LowBarBarrier: 30,
                        OI.k_MoatBarrier: 40,
                        OI.k_RoughTerrainBarrier: 40,
                        OI.k_RockWallBarrier: -75,
                        OI.k_PortcullisBarrier: 30,
                        OI.k_RampartsBarrier: -50,
                        } [self.barrierType]
        return barrierSpeed

    def getTurnAngle(self):
        """ returns the angle required to turn toward the tower
        in order to initiate a shot. Note that this can only
        be approximate since we don't currently understand how much
        our heading has been affected by the barrier crossing. Positive
        angles signify a rightward turn.
        """
        turnAngle = {
                    1: 80.4,
                    2: 41.08,
                    3: 11.95,
                    4: -13.12,
                    5: -57.75,
                    } [self.position]
