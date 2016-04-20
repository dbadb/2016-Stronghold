import wpilib
from wpilib import buttons
import commands.portcullisCmds as pcc

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
        self.initSmartDashboard()

    def initDriveTrain(self):
        pass

    def initLauncher(self):
        pass

    def initPortcullis(self):
        s = self.aimStick
        self.pcUpButton = buttons.JoystickButton(s, OI.k_pcUpButton)
        self.pcUpButton.whenPressed(pcc.MoveUp(self.robot))

        self.pcDownButton = buttons.JoystickButton(s, OI.k_pcDownButton)
        self.pcDownButton.whenPressed(pcc.MoveDown(self.robot))

        self.pcBarInButton = buttons.JoystickButton(s, OI.k_pcBarInButton)
        self.pcBarInButton.whenPressed(pcc.BarIn(self.robot))

        self.pcBarOutButton = buttons.JoystickButton(s, OI.k_pcBarOutButton)
        self.pcBarOutButton.whenPressed(pcc.BarOut(self.robot))

        self.pcBarStopButton = buttons.JoystickButton(s, OI.k_pcBarStopButton)
        self.pcBarStopButton.whenPressed(pcc.BarStop(self.robot))

    def initSmartDashboard(self):
        pass
