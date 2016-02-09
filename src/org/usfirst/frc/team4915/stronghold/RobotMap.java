package org.usfirst.frc.team4915.stronghold;

import edu.wpi.first.wpilibj.AnalogGyro;
import edu.wpi.first.wpilibj.CANTalon;
import edu.wpi.first.wpilibj.CANTalon.FeedbackDevice;
import edu.wpi.first.wpilibj.DigitalInput;
import edu.wpi.first.wpilibj.Encoder;
import edu.wpi.first.wpilibj.DoubleSolenoid;
import edu.wpi.first.wpilibj.RobotDrive;
import edu.wpi.first.wpilibj.RobotDrive.MotorType;
import edu.wpi.first.wpilibj.Servo;
import edu.wpi.first.wpilibj.interfaces.Gyro;


// RobotMap should only contain simple static  constant values
// Its purpose is to centralize 'wiring choices', so that wiring
// changes only impact this file.
public class RobotMap {
    // Define channels for the drive train motors
    public static final int DRIVETRAIN_RIGHT_BACK_MOTOR = 13;  
    public static final int DRIVETRAIN_RIGHT_FRONT_MOTOR = 12;
    public static final int DRIVETRAIN_LEFT_BACK_MOTOR = 11;
    public static final int DRIVETRAIN_LEFT_FRONT_MOTOR = 10;

    // Solenoid for two speed gear system for the drive train
    public static final int SOLENOID_CHANNEL_PRIMARY = 0;
    public static final int SOLENOID_CHANNEL_SECONDARY = 1;

    /* Gyro specific constants - Initialization takes place in RobotMapInit() */ 
    public final static int GYRO_PORT = 0;

    private static final int PLACEHOLDER_NUMBER = 69;
    
    /* IntakeLauncher specific constants - Initialization takes place in RobotMapInit() */ 
    /* FIXME: Initialize IntakeLauncher's ports */ 
    
    public static final int INTAKE_LEFT_MOTOR_PORT = PLACEHOLDER_NUMBER; // TODO
    public static final int INTAKE_RIGHT_MOTOR_PORT = PLACEHOLDER_NUMBER; // TODO
    public static final int AIM_MOTOR_PORT = PLACEHOLDER_NUMBER; // TODO

    public static final int BOULDER_SWITCH_PORT = PLACEHOLDER_NUMBER; // TODO
    public static final int LAUNCHER_BOTTOM_SWITCH_PORT = PLACEHOLDER_NUMBER; // TODO
    public static final int LAUNCHER_TOP_SWITCH_PORT = PLACEHOLDER_NUMBER; // TODO

    public static final int LAUNCHER_SERVO_PORT = PLACEHOLDER_NUMBER; // TODO
    // not actual port values

    public static final double AIM_MOTOR_FORWARD_SOFT_LIMIT = 99999999.99; // TODO
    public static final double AIM_MOTOR_REVERSE_SOFT_LIMIT = 99999999.99; // TODO
    public static final double AIM_MOTOR_P = 0; //TODO
    public static final double AIM_MOTOR_I = 0; //TODO
    public static final double AIM_MOTOR_D = 0; //TODO


}
