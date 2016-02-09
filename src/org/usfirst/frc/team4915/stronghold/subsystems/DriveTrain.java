
package org.usfirst.frc.team4915.stronghold.subsystems;

import edu.wpi.first.wpilibj.AnalogGyro;
import edu.wpi.first.wpilibj.CANTalon;
import edu.wpi.first.wpilibj.Joystick;
import edu.wpi.first.wpilibj.RobotDrive;
import edu.wpi.first.wpilibj.RobotDrive.MotorType;
import edu.wpi.first.wpilibj.command.Subsystem;
import edu.wpi.first.wpilibj.interfaces.Gyro;
import edu.wpi.first.wpilibj.smartdashboard.SmartDashboard;
import org.usfirst.frc.team4915.stronghold.RobotMap;
import org.usfirst.frc.team4915.stronghold.commands.ArcadeDrive;

import java.util.Arrays;
import java.util.List;

public class DriveTrain extends Subsystem {
	
    public RobotDrive robotDrive;
    
    public Gyro gyro;
    public double deltaGyro = 0;
    public double gyroHeading = 0;
    public double startingAngle = 0;
    
    public CANTalon leftBackMotor; 
    public CANTalon rightBackMotor; 
    public CANTalon leftFrontMotor; 
    public CANTalon rightFrontMotor;
    
    public List<CANTalon> motors;
    
  	public Joystick driveStick;
    public double joystickThrottle;
    
	
    // Constructor
	public DriveTrain(Joystick driveStick)
	{
		this.driveStick = driveStick;

        this.gyro = new AnalogGyro(RobotMap.GYRO_PORT);
        
        this.leftBackMotor = new CANTalon(RobotMap.DRIVETRAIN_LEFT_BACK_MOTOR);
        this.rightBackMotor = new CANTalon(RobotMap.DRIVETRAIN_RIGHT_BACK_MOTOR);
        this.leftFrontMotor = new CANTalon(RobotMap.DRIVETRAIN_LEFT_FRONT_MOTOR);
        this.rightFrontMotor = new CANTalon(RobotMap.DRIVETRAIN_RIGHT_FRONT_MOTOR);
        
        /* 
         * TODO: Initialize the Talon drive motors
         * 1. establish follower mode: we have 4 motor controls, but need to give commands to two of them
         * 2. establish speed control mode
         * 3. on motors w/ encoders set feedbackdevice to quadEncoder
         * 4. optional: if driving jerky, set PID values
         */
        
        //follower mode for right side
        
        this.rightBackMotor.changeControlMode(CANTalon.TalonControlMode.Follower);
        this.rightBackMotor.set(this.rightFrontMotor.getDeviceID());
        //follow mode for left side
        this.leftBackMotor.changeControlMode(CANTalon.TalonControlMode.Follower);
        this.leftBackMotor.set(this.leftFrontMotor.getDeviceID());
    
        System.out.println("DriveTrain: Talons are in follower mode");
		this.motors = Arrays.asList(this.leftFrontMotor, this.leftBackMotor, 
	            				    this.rightFrontMotor, this.rightBackMotor);
		this.robotDrive = new RobotDrive(this.leftFrontMotor, this.leftBackMotor, 
 			   						this.rightFrontMotor, this.rightBackMotor);
	}

    @Override
    public void initDefaultCommand() {
        // Set the default command for a subsystem here.
        System.out.println("INFO: Initializing the ArcadeDrive");

        setDefaultCommand(new ArcadeDrive(this.driveStick, this));

        this.robotDrive.setSafetyEnabled(true);
        //inverting motors
        this.robotDrive.setInvertedMotor(MotorType.kFrontLeft, true);
        this.robotDrive.setInvertedMotor(MotorType.kRearLeft, true);
        this.robotDrive.setInvertedMotor(MotorType.kFrontRight, true);
        this.robotDrive.setInvertedMotor(MotorType.kRearRight, true);
        
        //checking to see the encoder values
        //this can be removed later. Used to debug
        if (motors.size() > 0){
            for (int i = 0; i < motors.size(); i++){
                System.out.println("The encoder value of motor " + i + " is " + motors.get(i).getEncPosition());
            }
        }
    }

    public double modifyThrottle() {
        double modifiedThrottle = 0.40 * (1.0 * this.driveStick.getAxis(Joystick.AxisType.kThrottle)) + 0.60;
        if (modifiedThrottle != this.joystickThrottle) {
            SmartDashboard.putNumber("Throttle: ", modifiedThrottle);
        }
        setMaxOutput(modifiedThrottle);
        return modifiedThrottle;
    }

    private void setMaxOutput(double topSpeed) {
        this.robotDrive.setMaxOutput(topSpeed);
    }

    public void arcadeDrive(Joystick stick) {
        this.trackGyro();
        this.robotDrive.arcadeDrive(stick);
        //checking to see the encoder values
        //this can be removed later. Used to debug
        if (motors.size() > 0){
            for (int i = 0; i < motors.size(); i++){
                System.out.println("The encoder value of motor " + i + " is " + motors.get(i).getEncPosition());
            }
        }
    }

    public void twistDrive(Joystick stick) {
        this.trackGyro();
        /*
         * FIXME: should use rotate values rather than twist values 1 to -1 --
         * check the motor mapping correctness
         */
        this.robotDrive.arcadeDrive(stick, Joystick.AxisType.kY.value, stick, Joystick.AxisType.kZ.value);
    }

    public void stop() {
        this.robotDrive.arcadeDrive(0, 0);
    }

    public void calibrateGyro() {
        this.gyro.reset();
    }

    // Methods for Gyro
    public double trackGyro() {
        this.gyroHeading = -gyro.getAngle() + this.startingAngle;
        System.out.println("Gyro Angle: " + gyro.getAngle());
        System.out.println("Gyro heading:" + this.gyroHeading);
        return this.gyroHeading;
    }

    public void driveStraight(double speed) {
        this.robotDrive.arcadeDrive(speed, 0);
    }

    public void turn(boolean left) {
        if (left) {
            this.robotDrive.arcadeDrive(0, -.5);
        } else {
            this.robotDrive.arcadeDrive(0, .5);
        }
    }
}
