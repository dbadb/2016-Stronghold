from wpilib.command import Subsystem
from wpilib import CANTalon

s_pctPowerUp = .8
s_pctPowerDown = -.6

class Portcullis(Subsystem):
    def __init__(self, robot, name = None):
        super().__init__(name = name)
        self.robot = robot

        self.leftMotor = CANTalon(robot.map.k_PcLeftMotorId)
        self.leftMotor.changeControlMode(CANTalon.ControlMode.PercentVbus);
        self.leftMotor.enableLimitSwitch(True, True);
        self.leftMotor.enableBrakeMode(True);
        self.leftMotor.configPeakOutputVoltage(+12.0, -12.0);
        self.leftMotor.setSafetyEnabled(False);

        self.rightMotor = CANTalon(robot.map.k_PcRightMotorId)
        self.rightMotor.changeControlMode(CANTalon.ControlMode.PercentVbus);
        self.rightMotor.enableLimitSwitch(True, True);
        self.rightMotor.enableBrakeMode(True);
        self.rightMotor.configPeakOutputVoltage(+12.0, -12.0);
        self.rightMotor.setSafetyEnabled(False);

        self.barMotor = CANTalon(robot.map.k_PcBarMotorId)
        self.barMotor.changeControlMode(CANTalon.ControlMode.PercentVbus);
        self.barMotor.enableBrakeMode(True);
        self.barMotor.setSafetyEnabled(False);

        # self.leftMotor.setForwardSoftLimit(PORTCULLIS_TOP);
        # self.leftMotor.setReverseSoftLimit(PORTCULLIS_BOT);
        # self.leftMotor.enableForwardSoftLimit(true);
        # self.leftMotor.enableReverseSoftLimit(true);

    def initDefaultCommand(self):
        # currently we don't have a default command
        pass

    def leftAtTop(self):
        return self.leftMotor.isFwdLimitSwitchClosed()

    def leftAtBottom(self):
        return self.leftMotor.isRevLimitSwitchClosed()

    def rightAtTop(self):
        return self.rightMotor.isFwdLimitSwitchClosed();

    def rightAtBottom(self):
        return self.rightMotor.isRevLimitSwitchClosed();

    def moveRightUp(self):
        self.rightMotor.set(s_pctPowerUp)
        if self.RightAtTop():
            self.StopRight()
            self.robot.log("Right Portcullis reached top")

    def moveRightDown(self):
        self.rightMotor.set(s_pctPowerDown)
        if self.RightAtBottom():
            self.StopRight()
            self.robot.log("Right Portcullis reached bottom")

    def stopRight(self):
        self.rightMotor.set(0)

    def moveLeftUp(self):
        self.leftMotor.set(s_pctPowerUp)
        if self.LeftAtTop():
            self.StopLeft()
            self.robot.log("Left Portcullis reached top")

    def moveLeftDown(self):
        self.leftMotor.set(s_pctPowerDown)
        if self.LeftAtBottom():
            self.StopLeft()
            self.robot.log("Left Portcullis reached bottom")

    def stopLeft(self):
        self.leftMotor.set(0)

    def barIn(self):
        if self.LeftAtBottom() and self.RightAtBottom():
            self.barMotor.set(s_barIn);
        else:
            self.StopBar()

    def barOut(self):
        self.barMotor.set(s_barOut)

    def stopBar(self):
        self.barMotor.set(0)
