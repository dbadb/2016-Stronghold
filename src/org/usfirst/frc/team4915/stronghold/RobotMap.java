package org.usfirst.frc.team4915.stronghold;

import edu.wpi.first.wpilibj.AnalogGyro;
import edu.wpi.first.wpilibj.CANTalon;
import edu.wpi.first.wpilibj.Encoder;
import edu.wpi.first.wpilibj.RobotDrive;
import edu.wpi.first.wpilibj.RobotDrive.MotorType;
import edu.wpi.first.wpilibj.interfaces.Gyro;
import edu.wpi.first.wpilibj.DigitalInput;
import edu.wpi.first.wpilibj.Solenoid;

public class RobotMap {
    // If you are using multiple modules, make sure to define both the port
    // number and the module. For example you with a rangefinder:
    // public static int rangefinderPort = 1;
    // public static int rangefinderModule = 1;

    // Define channels for the motors
    public static final int driveTrainLeftBackMotor = 12;
    public static final int driveTrainRightBackMotor = 10;
    public static final int driveTrainLeftFrontMotor = 13;
    public static final int driveTrainRightFrontMotor = 11;

    public static final CANTalon leftBackMotor = new CANTalon(driveTrainLeftBackMotor);
    public static final CANTalon rightBackMotor = new CANTalon(driveTrainRightBackMotor);
    public static final CANTalon leftFrontMotor = new CANTalon(driveTrainLeftFrontMotor);
    public static final CANTalon rightFrontMotor = new CANTalon(driveTrainRightFrontMotor);

    public static final RobotDrive drive = new RobotDrive(0, 1, 2, 3);

    static {
        //drive.setInvertedMotor(MotorType.kRearRight, true);
        //drive.setInvertedMotor(MotorType.kFrontRight, true);

        //drive.setInvertedMotor(MotorType.kRearLeft, true);
        //drive.setInvertedMotor(MotorType.kFrontLeft, true);
    }

    public final static int GYRO_PORT = 0;
    // gyro instantiation
    public final static Gyro gyro = new AnalogGyro(GYRO_PORT);

    private static final int INTAKE_LEFT_MOTOR_PORT = -1; // TODO
    private static final int INTAKE_RIGHT_MOTOR_PORT = -1; //TODO
    private static final int AIM_MOTOR_PORT = -1; // TODO

    private static final int BOULDER_SWITCH_PORT = -1; // TODO
    private static final int LAUNCHER_BOTTOM_SWITCH_PORT = -1; // TODO
    private static final int LAUNCHER_TOP_SWITCH_PORT = -1; // TODO

    private static final int LAUNCHER_SOLENOID_PORT = -1; // TODO
    // not actual port values

    public static CANTalon intakeLeftMotor = new CANTalon(INTAKE_LEFT_MOTOR_PORT);
    public static CANTalon intakeRightMotor = new CANTalon(INTAKE_RIGHT_MOTOR_PORT);
    public static CANTalon aimMotor = new CANTalon(AIM_MOTOR_PORT);

    public static DigitalInput boulderSwitch = new DigitalInput(BOULDER_SWITCH_PORT);
    public static DigitalInput launcherTopSwitch = new DigitalInput(LAUNCHER_TOP_SWITCH_PORT);
    public static DigitalInput launcherBottomSwitch = new DigitalInput(LAUNCHER_BOTTOM_SWITCH_PORT);

    public static Solenoid launcherSolenoid = new Solenoid(LAUNCHER_SOLENOID_PORT);

}
