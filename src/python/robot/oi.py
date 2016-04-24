import wpilib
from wpilib.buttons import JoystickButton
from wpilib import SendableChooser
from wpilib import SmartDashboard

import commands.driveTrainCmds as DTCmds
import commands.portcullisCmds as PCmds
import commands.intakeLauncherCmds as ILCmds
import commands.visionCmds as VCmds

class OI:
    """
    OI defines the operator interface for Ares.
        - two joysticks with many associated buttons
        - smartdashboard widgets
    """
    # Joysticks
    k_driveStickPort = 0
    k_launcherStickPort = 1

    # DriveStick Commands - controls for driver:
    #   move, turn, throttle, intake, drive, intake ball
    k_intakeBallButton = 3
    k_aimIntakeButton = 4
    k_driveStopIntakeWheelsButton = 5
    k_aimNeutralButton = 6
    k_turnThrottleButton = 8
    k_driveStrightButton = 11 # experimental

    # LauncherStick Commands - controls for mechanism operator:
    #   aim, shoot, portcullis
    k_lightSwitchButton = 2
    k_kickBallButton = 3
    k_spinIntakeWheelsOutButton = 4
    k_stopIntakeWheelsButton = 5
    k_pcUpButton = 6  # Pc is portcullis
    k_pcDownButton = 7
    k_pcBarStopButton = 9
    k_pcBarInButton = 10
    k_pcBarOutButton = 11

    # Auto positions are numbered (1-5), position 1 is special
    k_LowBarPosition = 1

    # Auto barrier
    k_LowBarBarrier = 0
    k_MoatBarrier = 1
    k_RoughTerrainBarrier = 2
    k_RockWallBarrier = 3
    k_PortcullisBarrier = 4
    k_RampartsBarrier = 5

    # Auto strategy
    k_NoMoveStrategy = 0
    k_CrossStrategy = 1
    k_CrossBlindShotStrategy = 2
    k_CrossVisionShotStrategy = 3

    def __init__(self, robot):
        self.robot = robot
        self.driveStick = wpilib.Joystick(OI.k_driveStickPort)
        self.aimStick = wpilib.Joystick(OI.k_launcherStickPort)

        self.initDriveTrain()
        self.initLauncher()
        self.initPortcullis()
        self.initAutonomous()
        self.initVision()

        self.initSmartDashboard()

    def initDriveTrain(self):
        ds = self.driveStick
        self.dtTurnThrottleButton = JoystickButton(ds, OI.k_turnThrottleButton)
        # TODO: convert whileHeld/whenRealsed pair to a single command
        self.dtTurnThrottleButton.whileHeld(DTCmds.TurnSpeedSlow(self.robot))
        self.dtTurnThrottleButton.whenReleased(DTCmds.TurnSpeedFast(self.robot))

    def initLauncher(self):
        aS = self.aimStick
        dS = self.driveStick

        self.kickBallButton = JoystickButton(aS, OI.k_kickBallButton)
        self.kickBallButton.whenPressed(ILCmds.LaunchBallCommandGroup(self.robot))

        # TODO: Java code had two buttons for stop wheels
        self.mechStopWheelsButton = JoystickButton(aS, OI.k_stopIntakeWheelsButton)
        self.mechStopWheelsButton.whenPressed(ILCmds.StopWheelsCommand(self.robot))

        self.grabBallButton = JoystickButton(dS, OI.k_intakeBallButton)
        self.grabBallButton.whenPressed(ILCmds.IntakeBallCommandGroup(self.robot))

        self.spinIntakeWheelsOutButton = JoystickButton(aS, OI.k_spinIntakeWheelsOutButton)
        self.spinIntakeWheelsOutButton.whenPressed(ILCmds.SpinIntakeWheelsCommand(self.robot, "out"))

        self.driveLauncherJumpToIntakeButton = JoystickButton(dS, OI.k_aimIntakeButton)
        self.driveLauncherJumpToIntakeButton.whenPressed(ILCmds.LauncherGoToIntakeCommand(self.robot))

        # TODO: Java code had two buttons for neutral
        self.driveLauncherJumpToNeutralButton = JoystickButton(aS, OI.k_aimNeutralButton)
        self.driveLauncherJumpToNeutralButton.whenPressed(ILCmds.LauncherGoToNeutralCommand(self.robot))

    def initVision(self):
        s = self.aimStick
        self.lightSwitchButton = JoystickButton(s, OI.k_lightSwitchButton)
        self.lightSwitchButton.whenPressed(VCmds.LightSwitchCmd(self.robot))

    def initPortcullis(self):
        s = self.aimStick
        self.pcUpButton = JoystickButton(s, OI.k_pcUpButton)
        self.pcUpButton.whenPressed(PCmds.MoveUp(self.robot))

        self.pcDownButton = JoystickButton(s, OI.k_pcDownButton)
        self.pcDownButton.whenPressed(PCmds.MoveDown(self.robot))

        self.pcBarInButton = JoystickButton(s, OI.k_pcBarInButton)
        self.pcBarInButton.whenPressed(PCmds.BarIn(self.robot))

        self.pcBarOutButton = JoystickButton(s, OI.k_pcBarOutButton)
        self.pcBarOutButton.whenPressed(PCmds.BarOut(self.robot))

        self.pcBarStopButton = JoystickButton(s, OI.k_pcBarStopButton)
        self.pcBarStopButton.whenPressed(PCmds.BarStop(self.robot))

    def initAutonomous(self):
        ch = SendableChooser()
        ch.addDefault("1: Low Bar", self.k_LowBarPosition)
        ch.addObject("2", 2)
        ch.addObject("3", 3)
        ch.addObject("4", 4)
        ch.addObject("5", 5)
        self.startingFieldPosition = ch

        ch = SendableChooser()
        ch.addDefault("Low Bar", self.k_LowBarBarrier)
        ch.addObject("Moat", self.k_MoatBarrier)
        ch.addObject("Rough Terrain", self.k_RoughTerrainBarrier)
        ch.addObject("Rock Wall", self.k_RockWallBarrier)
        ch.addObject("Portcullis", self.k_PortcullisBarrier)
        ch.addObject("Ramparts", self.k_RampartsBarrier)
        self.barrierType = ch

        ch = SendableChooser()
        ch.addDefault("None", self.k_NoMoveStrategy)
        ch.addObject("Cross Only", self.k_CrossStrategy)
        ch.addObject("Cross, Blind Shot", self.k_CrossBlindShotStrategy)
        ch.addObject("Cross, Vision Shot",self.k_CrossVisionShotStrategy)
        self.strategy = ch

    def initSmartDashboard(self):
        SmartDashboard.putData("AutoFieldPosition", self.startingFieldPosition)
        SmartDashboard.putData("AutoBarrierType", self.barrierType)
        SmartDashboard.putData("AutoStrategy", self.strategy)

        # TODO: something about build (user, date, version)
