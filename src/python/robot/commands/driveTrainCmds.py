from wpilib.command import Command
from wpilib import Joystick
from visionstate import VisionState

class JoystickDriver(Command):

    def __init__(self, robot):
        self.robot = robot
        self.driveStick = robot.oi.driveStick
        self.driveTrain = robot.driveTrain
        self.requires(self.driveTrain)

    # initialize: called just before this Command runs the first time
    def initialize(self):
        self.robot.info("JoystickDriver initialize speed mode")
        self.driveTrain.initForCommand(self.driveTrain.k_ControlModeSpeed)

    # execute: called repeatedly when this Command is scheduled to run
    def execute(self):
        vs = VisionState.getInstance()
        if vs.wantsControl:
            self.driveTrain.endAutoTurn()
            self.driveTrain.trackVision()
        else:
            jx = self.driveStick.getX()
            jy = self.driveStick.getY()
            throttle = self.driveStick.getThrottle()
            self.driveTrain.joystickDrive(jx, -jy, throttle)

    # JoystickDriver never isFinished (unless 'requred'/interrupted)
    def isFinished(self):
        return False

    # end: called once after isFinished returns true
    def end(self):
        self.driveTrain.stop()
        self.robot.info("JoystickDriver end")

    # interrupted: called when another command which requires one or more of the same
    #   subsystems is scheduled to run
    def interrupted(self):
        self.end()
        self.robot.info("JoystickDriver interrupted")

class JoystickDriveStraight(Command):
    """DriveStraight: This class is a test of whether the IMU can be relied upon to
        assist the driver (or autonomous) to drive straight over
        complex barriers like the ramparts.
        Note: this is experimental and assumes that the command is
        bound to a whilePressed joystick button.
    """
    def __init__(self, robot):
        self.robot = robot
        self.driveTrain = robot.driveTrain
        self.requires(self.driveTrain)
        self.setInterruptible(True)
        self.isRunning = False
        self.initialHeading = None
        self.driveStick = robot.oi.driveStick

    def initialize(self):
        self.robot.info("JoystickDriveStraight: initialize speed mode")
        if not self.isRunning:
            self.initialHeading = self.driveTrain.getHeading()
            self.isRunning = True
        self.driveTrain.initForCommand(self.driveTrain.k_SpeedMode)

    def execute(self):
        deltaHeading = self.driveTrain.getHeading() - self.initialHeading
        curve = deltaHeading * -.3 # a correction strength
        outputMagnitude = -.35 * self.joystickDrive.getY()
        self.driveTrain.drive(outputMagnitude, curve)

    def isFinished(self):
        return False  # for use in "whilePressed" situaions

    def end(self):
        self.isRunning = False
        self.robot.info("JoystickDriveStraight: end")

    def interrupted():
        self.robot.info("JoystickDriveStraight: interrupted")
        self.robot.end()

class AutoDriveStraight(Command):
    k_maxRetries = 100 # number of executes to wait 'til encoder resets
    def __init__(self, robot, distanceInInches, speed):
        self.robot = robot
        self.driveTrain = robot.driveTrain
        self.intakeLauncher = robot.intakeLauncer
        self.requires(self.driveTrain)
        self.distanceInTicks = self.driveTrain.inchesToTicks(distanceInInches)
        self.speed = speed
        self.retryCount = 0

    def initialize(self):
        self.robot.info("AutoDriveStraight initialize")
        self.isDone = False
        self.isInitialized = False
        self.driveTrain.initForCommand(self.driveTrain.k_ControlModeSpeed)
        self.intakeLauncher.startAutoDrive()

    def execute(self):
        if self.isDone:
            self.driveTrain.stop()
            return

        if not self.isInitialized:
            if self.driveTrain.encodersAreZero():
                self.isInitialized = True
            else:
                self.retryCount = self.retryCount + 1
                if self.retryCount > self.k_maxRetries:
                    self.robot.error("AutoDriveStraight: INITIALIZED FAILED, MAXED OUT RETRIES")
                    self.isDone = True
        elif self.driveTrain.destinationReached(self.distanceInTicks):
            self.info("AutoDriveStraight: arrived")
            self.isDone = True
        else:
            self.driveTrain.driveStraight(self.speed)

    def isFinished(self):
        return self.isDone

    def interrupted(self):
        self.robot.info("AutoDriveStraight interrupted")
        self.end()

    def end(self):
        self.robot.info("AutoDriveStraight end")
        self.isDone = True
        self.driveTrain.stop()
