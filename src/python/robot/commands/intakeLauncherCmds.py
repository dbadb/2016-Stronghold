from wpilib.command import Command


class LightSwitchCmd(Command):
    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        self.enabled = False

    def initialize(self):
        pass

    def execute(self):
        self.enabled = not self.enabled
        self.robot.info("light is now: " + self.enabled)
        self.robot.setLight(self.enabled)

    def isFinished(self):
        return True   # we're a one-shot

    def end(self):
        pass

    def interrupted(self):
        pass
