
from wpilib.command import Subsystem
from wpilib import SmartDashboard
from wpilib import CANTalon
from wpilib import LiveWindow
from wpilib import Servo
from wpilib import DigitalInput

import commands.intakeLauncherCmds as ILCmds

import math

class IntakeLauncher(Subsystem):
    """A class to manage/control all aspects of shooting boulders.

    IntakeLauncher is comprised of:
        aimer: to raise & lower the mechanism for ball intake and shooting
        wheels: to suck or push the boulder
        launcher: to push boulder into the wheels during shooting
        limit switches: to detect if aimer is at an extreme position
        potentiometer: to measure our current aim position
        boulderSwitch: to detect if boulder is present

    Aiming is controlled via two modes
        1: driver/interactive: aimMotor runs in VBUS mode to change angle
        2: auto/vision control: aimMotor runs in closed-loop position mode
           to arrive at a designated position
    """

    k_launchMin = 684.0         # manual calibration value
    k_launchMinDegrees = -11    # ditto (vestigial)
    k_launchMax = 1024.0        # manual calibration value
    k_launchMaxDegrees = 45       # ditto (vestigial)
    k_launchRange = k_launchMax - k_launchMin
    k_launchRangeDegrees = k_launchMaxDegrees - k_launchMinDegrees
    k_aimDegreesSlop = 2                # TODO: tune this

    k_intakeSpeed = -.60                # pct vbux
    k_launchSpeedHigh = 1.0             # pct vbus
    k_launchSpeedLow = .7
    k_launchSpeedZero = 0
    k_servoLeftLaunchPosition = .45 # servo units
    k_servoRightLaunchPosition = .65
    k_servoLeftNeutralPosition = .75
    k_servoRightNeutralPosition = .4
    k_aimMultiplier = .5
    k_maxPotentiometerError = 5 # potentiometer units

    # launcher positions are measured as a percent of the range
    # of the potentiometer..
    #  intake: an angle approriate for intaking the boulder
    #  neutral: an angle appropriate for traversing the lowbar
    #  travel:  an angle appropriate for traversing the rockwall, enableLimitSwitch
    #  highgoal threshold: above which we shoot harder
    k_launchIntakeRatio = 0.0
    k_launchTravelRatio = .51
    k_launchNeutralRatio = .51
    k_launchHighGoalThreshold = .69

    def __init__(self, robot, name=None):
        super().__init__(name=name)
        self.robot = robot
        self.launchMin = self.k_launchMin
        self.launchMax = self.k_launchMax
        self.launchRange = self.launchMax - self.launchMin
        self.controlMode = None
        self.visionState = robot.visionState

        self.intakeLeftMotor = CANTalon(robot.map.k_IlLeftMotorId)
        self.intakeLeftMotor.changeControlMode(CANTalon.ControlMode.PercentVbus)
        self.intakeLeftMotor.reverseSensor(True)
        self.intakeLeftMotor.setSafetyEnabled(False)

        self.intakeRightMotor = CANTalon(robot.map.k_IlRightMotorId)
        self.intakeRightMotor.changeControlMode(CANTalon.ControlMode.PercentVbus)
        self.intakeRightMotor.setSafetyEnabled(False)

        self.aimMotor = CANTalon(robot.map.k_IlAimMotorId)
        #LiveWindow.addActuator("IntakeLauncher", "AimMotor", self.aimMotor)
        if self.aimMotor.isSensorPresent(CANTalon.FeedbackDevice.AnalogPot):
            self.aimMotor.setSafetyEnabled(False)
            self.aimMotor.setFeedbackDevice(CANTalon.FeedbackDevice.AnalogPot)
            self.aimMotor.enableLimitSwitch(True, True)
            self.aimMotor.enableBrakeMode(True)
            self.aimMotor.setAllowableClosedLoopErr(5)
            self.aimMotor.configPeakOutpuVoltage(12.0, -12.0)
            self.aimMotor.setVoltageRampRate(150)
            # TODO: setPID if needed

        self.boulderSwitch = DigitalInput(robot.map.k_IlBoulderSwitchPort)
        self.launcherServoLeft = Servo(robot.map.k_IlServoLeftPort)
        self.launcherServoRight = Servo(robot.map.k_IlServoRightPort)

    def initDefaultCommand(self):
        self.setDefaultCommand(ILCmds.DriverControlCommand(self.robot))

    def updateDashboard(self):
        pass

    def beginDriverControl(self):
        self.setControlMode("vbus")

    def driverControl(self, deltaX, deltaY):
        if self.robot.visionState.wantsControl():
            self.trackVision()
        else:
            self.setControlMode("vbus")
            self.aimMotor.set(deltaY * self.k_aimMultiplier)

    def endDriverControl(self):
        self.aimMotor.disableControl()

    # ----------------------------------------------------------------------
    def trackVision(self):
        if not self.visionState.TargetAcquired:
            return # hopefully someone is guiding the drivetrain to help acquire

        if not self.visionState.LauncherLockedOnTarget:
            if math.fabs(self.visionState.TargetY - self.getAngle()) < self.k_aimDegreesSlop:
                self.visionState.LauncherLockedOnTarget = True
            else:
                self.setPosition(self.degreesToTicks(self.TargetY))
        elif self.visionState.DriveLockedOnTarget:
            # here we shoot and then leave AutoAimMode
            pass
        else:
            # do nothing... waiting form driveTrain to reach orientation
            pass

    def setControlMode(self, mode):
        if mode != self.controlMode:
            self.controlMode = mode
            if mode == "vbus":
                self.aimMotor.disableControl()
                self.aimMotor.changeControlMode(CANTalon.ControlMode.PercentVbus)
                self.aimMotor.enableControl()
            elif mode == "position":
                self.aimMotor.disableControl()
                self.aimMotor.changeControlMode(CANTalon.ControlMode.Position)
                self.aimMotor.enableControl()
            elif mode == "disabled":
                self.aimMotor.disableControl()
            else:
                self.robot.error("ignoring controlmode " + mode)
                self.controlMode = None
                self.aimMotor.disableControl()

    # launcher aim -------------------------------------------------------------
    def getPosition(self):
        return self.aimMotor.getPosition()

    def getAngle(self):
        pos = self.getPosition()
        return self.ticksToDegress(pos)

    def setPosition(self, pos):
        self.setControlMode("position")
        self.aimMotor.set(pos)

    def isLauncherAtTop(self):
        return self.aimMotor.isFwdLimitSwitchClosed()

    def isLauncherAtBottom(self):
        return self.aimMotor.isRevLimitSwitchClosed()

    def isLauncherAtIntake(self):
        if self.k_intakeRatio == 0.:
            return self.isLauncherAtBottom()
        else:
            return self.isLauncherNear(self.getIntakePosition())

    def isLauncherAtNeutral(self):
        return self.isLauncherNear(self.getNeutralPosition())

    def isLauncherAtTravel(self):
        return self.isLauncherNear(self.getTravelPosition())

    def isLauncherNear(self, pos):
        return math.fabs(self.getPosition()-pos) < self.k_maxPotentiometerError

    def getIntakePosition(self):
        return self.getLauncherPositionFromRatio(self.k_launchIntakeRatio)

    def getNeutralPosition(self):
        return self.getLauncherPositionFromRatio(self.k_launchNeutralRatio)

    def getTravelPosition(self):
        return self.getLauncherPositionFromRatio(self.k_launchTravelRatio)

    def getLauncherPositionFromRatio(self, ratio):
        return self.launchMin + ratio * self.launchRange

    def degressToTicks(self, deg):
        ratio = (deg - self.k_launchMinDegrees) / self.k_launchRangeDegrees
        return self.k_launchMin + ratio * self.k_launchRange

    def ticksToDegrees(self, t):
        ratio = (t - self.k_launchMin) / self.k_launchRange
        return self.k_launchMinDegrees + ratio * self.k_launchRangeDegrees

    def calibratePotentiometer(self):
        if self.isLauncherAtBottom():
            self.launchMin = self.getPosition()
        elif self.isLauncherAtTop():
            self.launchMax = self.getPosition()
        self.launchRange = self.launchMax - self.launchMin

    # intake wheels controls ---------------------------------------------------
    def setWheelSpeedForLaunch(self):
        if self.isLauncherAtTop():
            speed = self.k_launchSpeedHigh
        else:
            speed = self.k_launchSpeedLow
        self.setSpeed(speed)

    def setWheelSpeedForIntake(self):
        self.setSpeed(self.k_intakeSpeed)

    def stopWheels(self):
        self.setSpeed(k_launchSpeedZero)

    def setWheelSpeed(self, speed):
        self.intakeLeftMotor.set(speed)
        self.intakeRightMotor.set(-speed)

    # boulder and launcher servo controls --------------------------------------------------
    def hasBoulder(self):
        return self.boulderSwitch.get()

    def activateLauncherServos(self):
        self.robot.info("activateLauncherServos at:" + self.getAimPosition())
        self.launcherServoLeft.set(self.k_servoLeftLaunchPosition)
        self.launcherServoRight.set(self.k_servoRightLaunchPosition)

    def retractLauncherServos(self):
        self.launcherServoLeft.set(self.k_servoLeftNeutralPosition)
        self.launcherServoRight.set(self.k_servoRightNeutralPosition)
