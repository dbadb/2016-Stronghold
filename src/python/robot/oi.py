import wpilib
from wpilib import buttons
from wpilib import SendableChooser

import commands.portcullisCmds as PCmds
import commands.intakeLauncherCmds as ILCmds

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


    def __init__(self, robot):
        self.robot = robot
        self.driveStick = wpilib.Joystick(OI.k_driveStickPort)
        self.aimStick = wpilib.Joystick(OI.k_launcherStickPort)

        self.initDriveTrain()
        self.initLauncher()
        self.initPortcullis()
        self.initAutonomous()

        self.initSmartDashboard()

    def initDriveTrain(self):
        pass

    def initLauncher(self):
        s = self.aimStick
        self.lightSwitchButton = buttons.JoystickButton(s, OI.k_lightSwitchButton)
        self.lightSwitchButton.whenPressed(ILCmds.LightSwitchCmd(self.robot))

    def initPortcullis(self):
        s = self.aimStick
        self.pcUpButton = buttons.JoystickButton(s, OI.k_pcUpButton)
        self.pcUpButton.whenPressed(PCmds.MoveUp(self.robot))

        self.pcDownButton = buttons.JoystickButton(s, OI.k_pcDownButton)
        self.pcDownButton.whenPressed(PCmds.MoveDown(self.robot))

        self.pcBarInButton = buttons.JoystickButton(s, OI.k_pcBarInButton)
        self.pcBarInButton.whenPressed(PCmds.BarIn(self.robot))

        self.pcBarOutButton = buttons.JoystickButton(s, OI.k_pcBarOutButton)
        self.pcBarOutButton.whenPressed(PCmds.BarOut(self.robot))

        self.pcBarStopButton = buttons.JoystickButton(s, OI.k_pcBarStopButton)
        self.pcBarStopButton.whenPressed(PCmds.BarStop(self.robot))

    def initAutonomous(self):
        ch = SendableChooser()
        ch.addDefault("1: Low Bar", 1)
        ch.addObject("2", 2)
        ch.addObject("3", 3)
        ch.addObject("4", 4)
        ch.addObject("5", 5)
        self.startingFieldPosition = ch

        ch = SendableChooser()
        ch.addDefault("Low Bar", "lowbar")
        ch.addObject("Moat", "moat")
        ch.addObject("Rough Terrain", "roughTerrain")
        ch.addObject("Rock Wall", "rockWall")
        ch.addObject("Portcullis", "portcullis")
        ch.addObject("Ramparts", "ramparts")
        self.barrierType = ch

        ch = SendableChooser()
        ch.addDefault("None", "none")
        ch.addObject("Cross Only", "crossOnly")
        ch.addObject("Cross, Blind Shot", "crossBlindShot")
        ch.addObject("Cross, Vision Shot", "crossVisionShot")
        self.strategy = ch


    def initSmartDashboard(self):
        pass
