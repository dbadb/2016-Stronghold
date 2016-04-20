
from wpilib.command import Subsystem
from wpilib import RobotDrive
from wpilib import LiveWindow
from wpilib import PIDController
from wpilib import CANTalon
from utils.bno055 import BNO055
from commands.driveTrainCmds import JoystickDriver

import math

class DriveTrain(Subsystem):
    """DriveTrain: is the subsystem responsible for motors and
       devices associated with driving subystem.

       As a subsystem, we represent the single point of contact
       for all drivetrain-related controls.  Specifically, commands
       that manipulate the drivetrain should 'require' the singleton
       instance (via require(robot.driveTrain)).  Unless overridden,
       our default command, JoystickDriver, is the means by which
       driving occurs.
   """

    k_minThrottleScale = 0.5
    k_defaultDriveSpeed = 100.0 # ~13.0 ft/sec determined experimentally
    k_maxDriveSpeed = 150.0     # ~20 ft/sec
    k_maxTurnSpeed = 40.0       # ~3-4 ft/sec
    k_fastTurn = -1
    k_mediumTurn = -.72
    k_slowTurn = -.55
    k_quadTicksPerWheelRev = 9830
    k_wheelDiameterInInches = 14.0
    k_wheelCircumferenceInInches = k_wheelDiameterInInches * math.pi
    k_quadTicksPerInch = k_quadTicksPerWheelRev / k_wheelCircumferenceInInches

    k_turnKp = .1
    k_turnKi = 0
    k_turnKd = .3
    k_turnKf = .001

    k_ControlModeSpeed=0,
    k_ControlModeVBus=1

    class TurnHelper():
        """TurnHelper: a private helper class for PIDController-based
           imu-guided turning.
        """
        def __init__(self, driveTrain):
            self.driveTrain = driveTrain

        def pidWrite(self, output):
            self.driveTrain.turn(output * DriveTrain.k_maxTurnSpeed)

    def __init__(self, robot, name=None):
        super().__init__(name=name)
        self.robot = robot
        # STEP 1: instantiate the motor controllers
        self.leftMasterMotor = CANTalon(robot.map.k_DtLeftMasterId)
        self.leftFollowerMotor = CANTalon(robot.map.k_DtLeftFollowerId)

        self.rightMasterMotor = CANTalon(robot.map.k_DtRightMasterId)
        self.rightFollowerMotor = CANTalon(robot.map.k_DtRightFollowerId)

        # Step 2: Configure the follower Talons: left & right back motors
        self.leftFollowerMotor.changeControlMode(CANTalon.ControlMode.Follower)
        self.leftFollowerMotor.set(self.leftMasterMotor.getDeviceID())

        self.rightFollowerMotor.changeControlMode(CANTalon.ControlMode.Follower)
        self.rightFollowerMotor.set(self.rightMasterMotor.getDeviceID())

        # STEP 3: Setup speed control mode for the master Talons
        self.leftMasterMotor.changeControlMode(CANTalon.ControlMode.Speed)
        self.rightMasterMotor.changeControlMode(CANTalon.ControlMode.Speed)

        # STEP 4: Indicate the feedback device used for closed-loop
        # For speed mode, indicate the ticks per revolution
        self.leftMasterMotor.setFeedbackDevice(CANTalon.FeedbackDevice.QuadEncoder)
        self.rightMasterMotor.setFeedbackDevice(CANTalon.FeedbackDevice.QuadEncoder)
        self.leftMasterMotor.configEncoderCodesPerRev(self.k_quadTicksPerWheelRev)
        self.rightMasterMotor.configEncoderCodesPerRev(self.k_quadTicksPerWheelRev)

        # STEP 5: Set PID values & closed loop error
        self.leftMasterMotor.setPID(0.22, 0, 0)
        self.rightMasterMotor.setPID(0.22, 0, 0)

        # Add ramp up rate
        self.leftMasterMotor.setVoltageRampRate(48.0) # max allowable voltage
                                                      # change /sec: reach to
                                                      # 12V after 1sec
        self.rightMasterMotor.setVoltageRampRate(48.0)

        # Add SmartDashboard controls for testing
        # Add SmartDashboard live windowS
        LiveWindow.addActuator("DriveTrain",
                              "Left Master %d" % robot.map.k_DtLeftMasterId,
                              self.leftMasterMotor)
        LiveWindow.addActuator("DriveTrain",
                                "Right Master %d" % robot.map.k_DtRightMasterId,
                                self.rightMasterMotor)

        # init RobotDrive - all driving should occur through its methods
        # otherwise we expect motor saftey warnings
        self.robotDrive = RobotDrive(self.leftMasterMotor, self.rightMasterMotor)
        self.robotDrive.setSafetyEnabled(True)

        # init IMU - used for driver & vision feedback as well as for
        #   some autonomous modes.
        self.imu = BNO055()
        self.turnPID = PIDController(self.k_turnKp, self.k_turnKd, self.k_turnKf,
                                     self.imu, DriveTrain.TurnHelper(self))
        self.turnPID.setOutputRange(-1, 1)
        self.turnPID.setInputRange(-180, 180)
        self.turnPID.setPercentTolerance(2)

        self.maxSpeed = self.k_defaultDriveSpeed
        # self.setContinuous() ?

        robot.info("Initialized DriveTrain")

    def initForCommand(self, controlMode):
        self.leftMasterMotor.setEncPosition(0) # async call
        self.rightMasterMotor.setEncPosition(0)
        self.robotDrive.StopMotor()
        self.robotDrive.setMaxOutput(self.maxSpeed)
        if controlMode == self.k_ControlModeSpeed:
            self.leftMasterMotor.changeControlMode(CANTalon.ControlMode.Speed)
            self.rightMasterMotor.changeControlMode(CANTalon.ControlMode.Speed)
        elif controlMode == self.k_ControlModeVBus:
            self.leftMasterMotor.changeControlMode(CANTalon.ControlMode.PercentVbus)
            self.rightMasterMotor.changeControlMode(CANTalon.ControlMode.PercentVbus)
        else:
            self.robot.error("Unexpected control mode")

        self.robot.info("driveTrain initDefaultCommand, controlmodes: %d %d" %
                        self.leftMasterMotor.getControlMode(),
                        self.rightMasterMotor.getControlMode())

    def initDefaultCommand(self):
        # control modes are integers values:
        #   0 percentvbux
        #   1 position
        #   2 velocity
        self.setDefaultCommand(JoystickDriver(self))
        self.robotDrive.stopMotor();

    def joystickDrive(self, jsY, jsX, throttle):
        """ joystickDrive - called by JoystickDriver command. Inputs
        are always on the range [-1, 1]... These values can be scaled
        for a better "feel", but should always be in a subset of this
        range.
        """
        if self.robot.isAutonomous or \
            (math.fabs(jx) < 0.075 and math.fabs(jy) < .075):
            # joystick dead zone or auto (where we've been scheduled via
            # default command machinery)
            self.robotDrive.stop()
        else:
            st = self.scaleThrottle(throttle)
            self.robotDrive.arcadeDrive(jsY*self.turnMultiplier, jsX*st)

    def drive(self, outputmag, curve):
        """ drive - used by drivestraight command..
        """
        self.robotDrive.drive(outputmag, curve)

    def driveStraight(self, speed):
        pass

    def stop(self):
        self.robotdrive.stopMotor(0)

    def getCurrentHeading(self):
        """ getCurrentHeading returns a value between -180 and 180
        """
        return math.degrees(self.imu.getHeading())  # getHeading:  -pi, pi

    def scaleThrottle(self, rawThrottle):
        """ scaleThrottle:
        returns a scaled value between MIN_THROTTLE_SCALE and 1.0
        MIN_THROTTLE_SCALE must be set to the lowest useful scale value through experimentation
        Scale the joystick values by throttle before passing to the driveTrain
        +1=bottom position; -1=top position
        """
        # Throttle in the range of -1 to 1. We would like to change that to a
        # range of MIN_THROTTLE_SCALE to 1. #First, multiply the raw throttle
        # value by -1 to reverse it (makes "up" maximum (1), and "down" minimum (-1))
        # Then, add 1 to make the range 0-2 rather than -1 to +1
        # Then multiply by ((1-k_minThrottleScale)/2) to change the range to 0-(1-k_minThrottleScale)
        # Finally add k_minThrottleScale to change the range to k_minThrottleScale to 1
        #
        # Check the results are in the range of k_minThrottleScale to 1, and clip
        # it in case the math went horribly wrong.
        result = ((rawThrottle * -1) + 1) * ((1-self.k_minThrottleScale) / 2) + self.k_minThrottleScale
        if result < self.k_minThrottleScale:
            # Somehow our math was wrong. Our value was too low, so force it to the minimum
            result = self.k_mintThrottleScale
        elif result > 1:
            # Somehow our math was wrong. Our value was too high, so force it to the maximum
            result = 1.0
        return result

    def inchesToTicks(self, inches):
        return int(self.k_quadTicksPerInch * inches)

    def destinationReached(self, distance):
        return math.fabs(self.leftMasterMotor.getEncPosition()) >= distance or \
               math.fabs(self.rightMasterMotr.getEncPosition()) >= distance
