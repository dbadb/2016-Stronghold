from wpilib.command import Command
from wpilib.command import CommandGroup
from wpilib.command import WaitCommand
from wpilib import SmartDashboard

# command groups -------------------------------------------------------------
class IntakeBallCommandGroup(CommandGroup):
    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        self.addSequential(RetractLauncherServosCommand(robot))
        self.addSequential(LauncherGoToIntakeCommand(robot))
        self.addSequential(SpinIntakeWheelsCommand(robot, "in"))

    def initialize(self):
        self.robot.info("IntakBallCommandGroup initialize")
        super().initialize()

    def end(self):
        self.robot.info("IntakBallCommandGroup end")
        super().end()

class LaunchBallCommandGroup(CommandGroup):
    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        self.addSequential(ActivateLauncherServosCommand(robot))
        self.addSequential(WaitCommand(1)) # wait 1 sec before retracting
        self.addSequential(RetractLauncherServosCommand(robot))
        self.addSequential(StopWheelsCommand(robot))

    def initialize(self):
        self.robot.info("LaunchBallCommandGroup initialize")
        super().initialize()

    def end(self):
        self.robot.info("LaunchBallCommandGroup end")
        super().end()

# comamnds ------------------------------------------------------------------
class DriverControlCommand(Command):
    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        self.aimStick = robot.oi.aimStick
        self.intakeLauncher = robot.intakeLauncher
        self.requires(self.intakeLauncher)

    def initialize(self):
        self.robot.info("IntakeLauncher Driver Control init")
        self.intakeLauncher.beginDriverControl()

    def execute(self):
        self.intakeLauncher.driverControl(self.aimStick.getX(),
                                          self.aimStick.getY())

    def end(self):
        self.robot.info("IntakeLauncher Driver Control end")
        self.intakeLauncher.endDriverControl()

    def isFinished(self):
        return False #  persist 'til interrupted

    def interrupted(self):
        self.robot.info("IntakeLauncher Driver Control interrupted")
        self.end()

class stateChangeCmd(Command):
    """oneShot: assumes that all the 'action' occurs in initialize()"""
    def __init__(self):
        super().__init__()
    def execute(self): pass
    def isFinished(self): return True
    def end(self): pass
    def interrupted(self): pass

class ActivateLauncherServosCommand(stateChangeCmd):
    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        self.intakeLauncher = robot.intakeLauncher
        self.requires(self.intakeLauncher)

    def initialize(self):
        self.robot.info("ActivateLauncherServosCommand init")
        self.robot.intakeLauncher.activateLauncherServos()

class RetractLauncherServosCommand(stateChangeCmd):
    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        self.intakeLauncher = robot.intakeLauncher
        self.requires(self.intakeLauncher)

    def initialize(self):
        self.robot.info("RetractLauncherServosCommand init")
        self.robot.intakeLauncher.retractLauncherServos()

class StopWheelsCommand(stateChangeCmd):
    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        self.intakeLauncher = robot.intakeLauncher
        self.requires(self.intakeLauncher)

    def initialize(self):
        self.robot.info("StopWheelsCommand init")
        self.robot.intakeLauncher.stopWheels()
        self.robot.portcullis.stopBar()  # XXX: questionable access to subsystem?

class SpinIntakeWheelsCommand(Command):
    def __init__(self, robot, direction):
        super().__init__()
        self.robot = robot
        self.intakeLauncher = robot.intakeLauncher
        self.requires(self.intakeLauncher)
        self.direction = direction

    def initialize(self):
        self.robot.info("SpinIntakeWheelsCommand %s init" % self.direction)
        self.setTimeout(10) # TODO: finialize timing
        SmartDashboard.putString("Intakewheels spinning", self.direction)

    def execute(self):
        if self.direction == "in":
            self.intakeLauncher.setWheelSpeedForIntake()
            self.porcullis.barIn()
        else:
            self.intakeLauncher.setWheelSpeedForShot()

    def isFinished(self):
        return self.isTimedOut()

    def end(self):
        self.intakeLauncher.stopWheels()

    def interrupted(self):
        self.robot("SpinIntakeWheelsCommand %s interrupted" % self.direction)
        self.end()

class LauncherGoToPositionCommand(Command):
    def __init__(self, robot, position):
        super().__init__()
        self.robot = robot
        self.intakeLauncher = robot.intakeLauncher
        self.requires(self.intakeLauncher)
        self.position = position

    def initialize(self):
        self.intakeLauncher.setPosition(self.position)

    def execute(self):
        pass

    def isFinished(self):
        return self.intakeLauncher.isLauncherNear(self.position)

    def end(self):
        self.robot.info("launcher goto position end")
        self.intakeLauncher.setControlMode("disabled")

    def interrupted(self):
        self.robot.info("launcher goto position interrupted")
        self.end()

class LauncherGoToIntakeCommand(LauncherGoToPositionCommand):
    def __init__(self, robot):
        super().__init__(robot, robot.intakeLauncher.getIntakePosition())

    def initialize(self):
        self.robot.info("launcher goto intake init")
        super().initialize()

class LauncherGoToNeutralCommand(LauncherGoToPositionCommand):
    def __init__(self, robot):
        super().__init__(robot, robot.intakeLauncher.getNeutralPosition())

    def initialize(self):
        self.robot.info("launcher goto neutral init")
        super().initialize()

class LauncherGoToTravelCommand(LauncherGoToPositionCommand):
    def __init__(self, robot):
        super().__init__(robot, robot.intakeLauncher.getTravelPosition())

    def initialize(self):
        self.robot.info("launcher goto travel init")
        super().initialize()
