
class RobotMap:
    """
    The RobotMap is a mapping from the ports sensors and actuators are wired into
    to a variable name. This provides flexibility changing wiring, makes checking
    the wiring easier and significantly reduces the number of magic numbers
    floating around.
    """

    # CAN devices --------------------------------------------------
    # driveTrain
    k_DtLeftMasterId = 10
    k_DtLeftFollowerId = 11
    k_DtRightMasterId = 12
    k_DtRightFollowerId = 13

    # intake launcher
    k_IlLeftMotorId = 15
    k_IlRightMotorId = 14
    k_IlAimMotorId = 16

    # ports are on CAN devices
    k_IlBoulderSwitchPort = 0
    k_IlServoLeftPort = 0
    k_IlServoRightPort = 1

    # portcullis
    k_PcLeftMotorId = 17
    k_PcRightMotorId = 18
    k_PcBarMotorId = 19
    k_PcSpeed = .6

    # Digital Outputs ---------------------------------------------------
    k_VsPhotonicCannon = 4  # a DigitalOutput

    # NB: no code here!  This is just a central place for wiring decisions.
