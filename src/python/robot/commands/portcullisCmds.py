from wpilib.command import CommandGroup
from wpilib.command import Command

# portcullis groups -------------------------------------------------
# A command group requires all of the subsystems that each member requires.

k_timeOut = 2

class MoveUp(CommandGroup):
    def __init__(self, robot, name=None):
        super().__init__(name)
        self.addParallel(MoveUpRight(robot, "pur", k_timeOut))
        self.addParallel(MoveUpLeft(robot, "pul", k_timeOut))

class MoveDown(CommandGroup):
    def __init__(self, robot, name=None):
        super().__init__(name)
        self.addParallel(MoveDownRight(robot, "pdr", k_timeOut))
        self.addParallel(MoveDownLeft(robot, "pdr", k_timeOut))

# portcullis commands ---------------------------------------------
class MoveUpRight(Command):
    def __init__(self, robot, name=None, timeout=None):
        super().__init__(name, timeout)
        self.robot = robot
        self.portcullis = robot.portcullis
        self.requires(self.portcullis)

    def initialize(self): # called just before command runs the first time
        pass

    def execute(self):   # called repeatedly while scheduled
        self.portcullis.moveRightUp()

    def isFinished(self):
        return self.portcullis.rightAtTop()

    def end(self): # called once after isFinished returns true
        self.portcullis.stopRight()

    def interrupted(self):
        self.robot.log("portcullis.MoveUpRight interrupted")
        end()

class MoveDownRight(Command):
    def __init__(self, robot, name=None, timeout=None):
        super().__init__(name, timeout)
        self.robot = robot
        self.portcullis = robot.portcullis
        self.requires(self.portcullis)

    def initialize(self): # called just before command runs the first time
        pass

    def execute(self):   # called repeatedly while scheduled
        self.portcullis.moveRightDown()

    def isFinished(self):
        return self.portcullis.rightAtBottom()

    def end(self): # called once after isFinished returns true
        self.portcullis.stopRight()

    def interrupted(self):
        self.robot.log("portcullis.MoveDownRight interrupted")
        end()

class MoveUpLeft(Command):
    def __init__(self, robot, name=None, timeout=None):
        super().__init__(name, timeout)
        self.robot = robot
        self.portcullis = robot.portcullis
        self.requires(self.portcullis)

    def initialize(self): # called just before command runs the first time
        pass

    def execute(self):   # called repeatedly while scheduled
        self.portcullis.moveLeftUp()

    def isFinished(self):
        return self.portcullis.leftAtTop()

    def end(self): # called once after isFinished returns true
        self.portcullis.stopLeft()

    def interrupted(self):
        self.robot.log("portcullis.MoveUpLeft interrupted")
        end()

class MoveDownLeft(Command):
    def __init__(self, robot, name=None, timeout=None):
        super().__init__(name, timeout)
        self.robot = robot
        self.portcullis = robot.portcullis
        self.requires(self.portcullis)

    def initialize(self): # called just before command runs the first time
        pass

    def execute(self):   # called repeatedly while scheduled
        self.portcullis.moveLeftDown()

    def isFinished(self):
        return self.portcullis.leftAtTop()

    def end(self): # called once after isFinished returns true
        self.portcullis.stopLeft()

    def interrupted(self):
        self.robot.log("portcullis.MoveDownLeft interrupted")
        end()

class BarIn(Command):
    def __init__(self, robot, name=None, timeout=None):
        super().__init__(name, timeout)
        self.robot = robot
        self.portcullis = robot.portcullis
        self.requires(self.portcullis)

    def initialize(self): # called just before command runs the first time
        pass

    def execute(self):   # called repeatedly while scheduled
        self.portcullis.barIn()

    def isFinished(self):
        return False

    def end(self): # called once after isFinished returns true
        self.portcullis.stopBar()

    def interrupted(self):
        self.robot.log("portcullis.BardIn interrupted")
        end()

class BarOut(Command):
    def __init__(self, robot, name=None, timeout=None):
        super().__init__(name, timeout)
        self.robot = robot
        self.portcullis = robot.portcullis
        self.requires(self.portcullis)

    def initialize(self): # called just before command runs the first time
        pass

    def execute(self):   # called repeatedly while scheduled
        self.portcullis.barOut()

    def isFinished(self):
        return False

    def end(self): # called once after isFinished returns true
        self.portcullis.stopBar()

    def interrupted(self):
        self.robot.log("portcullis.BarOut interrupted")
        end()

class BarStop(Command):
    def __init__(self, robot, name=None, timeout=None):
        super().__init__(name, timeout)
        self.robot = robot
        self.portcullis = robot.portcullis
        self.requires(self.portcullis)

    def initialize(self): # called just before command runs the first time
        pass

    def execute(self):   # called repeatedly while scheduled
        self.portcullis.stopBar()

    def isFinished(self):
        return True

    def end(self): # called once after isFinished returns true
        self.portcullis.stopBar()

    def interrupted(self):
        self.robot.log("portcullis.BarStop interrupted")
        end()
