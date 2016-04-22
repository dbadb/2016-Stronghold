

from wpilib.command import CommandGroup

class AutonomousCmd1(CommandGroup):

    def __init__(self, robot):
        super().__init__()

        

        self.strat = "unknownStrat"
        self.position = "unknownPosition"
        self.type = "unknownType"
