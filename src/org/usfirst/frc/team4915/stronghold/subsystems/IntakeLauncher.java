package org.usfirst.frc.team4915.stronghold.subsystems;

import edu.wpi.first.wpilibj.CANTalon;
import edu.wpi.first.wpilibj.CANTalon.FeedbackDevice;
import edu.wpi.first.wpilibj.CANTalon.TalonControlMode;
import edu.wpi.first.wpilibj.DigitalInput;
import edu.wpi.first.wpilibj.Encoder;
import edu.wpi.first.wpilibj.Joystick;
import edu.wpi.first.wpilibj.Servo;
import edu.wpi.first.wpilibj.command.Subsystem;
import org.usfirst.frc.team4915.stronghold.RobotMap;
import org.usfirst.frc.team4915.stronghold.commands.IntakeLauncher.SetLauncherHeightCommand;

public class IntakeLauncher extends Subsystem {

    // Ranges -1 to 1, negative values are reverse direction
    // Negative speed indicates a wheel spinning inwards and positive speed
    // indicates a wheel spinning outwards.
    // Numbers are not correct
    private static final double INTAKE_SPEED = -1.0;
    private static final double LAUNCH_SPEED = 1.0;
    private static final double ZERO_SPEED = 0.0;
    private static final double JOYSTICK_SCALE = 1.0; // TODO
    private static final double LAUNCHER_SERVO_NEUTRAL_POSITION = 0.0; // TODO
    private static final double LAUNCHER_SERVO_LAUNCH_POSITION = 1.0; // TODO
    private static final double AIM_MOTOR_INCREMENT = 0; // TODO
    private static final double LAUNCHER_MIN_HEIGHT = 0; // TODO
    private static final double LAUNCHER_MAX_HEIGHT = 0; // TODO

    private boolean autoAim = false;

    public Joystick aimStick;

    // left and right are determined when standing behind the robot

    // These motors control flywheels that collect and shoot the ball
    public CANTalon intakeLeftMotor;
    public CANTalon intakeRightMotor;

    // This motor adjusts the angle of the launcher for shooting
    public CANTalon aimMotor;

    // limitswitch in the back of the basket that tells the robot when the
    // boulder is secure
    public DigitalInput boulderSwitch;

    // limitswitches that tell when the launcher is at the maximum or minumum
    // height
    public DigitalInput launcherBottomSwitch;
    public DigitalInput launcherTopSwitch;

    public Servo launcherServo;
    
    /* FIXME: to delete as the encoder connect directly to Talon */
    public Encoder aimEncoder;
    
    public IntakeLauncher(Joystick aimStick) {
        this.intakeLeftMotor = new CANTalon(RobotMap.INTAKE_LEFT_MOTOR_PORT);
        this.intakeRightMotor = new CANTalon(RobotMap.INTAKE_RIGHT_MOTOR_PORT);
        this.aimMotor = new CANTalon(RobotMap.AIM_MOTOR_PORT);
        this.launcherServo = new Servo(RobotMap.LAUNCHER_SERVO_PORT);
        // TODO: Initialize intakelauncher motors here, such as limit switches and encoders
        
        /* FIXME: to delete as the switches connect directly to Talon */
        this.boulderSwitch = new DigitalInput(RobotMap.BOULDER_SWITCH_PORT);
        this.launcherTopSwitch = new DigitalInput(RobotMap.LAUNCHER_TOP_SWITCH_PORT);
        this.launcherBottomSwitch = new DigitalInput(RobotMap.LAUNCHER_BOTTOM_SWITCH_PORT);

        /* FIXME: to delete as the encoder connect directly to Talon */
        this.aimEncoder = new Encoder(RobotMap.LAUNCHER_BOTTOM_SWITCH_PORT, 
        							  RobotMap.LAUNCHER_TOP_SWITCH_PORT, 
        							  false, Encoder.EncodingType.k4X);
        
        // setup the motor
        this.aimMotor.setFeedbackDevice(FeedbackDevice.QuadEncoder);
        this.aimMotor.setForwardSoftLimit(RobotMap.AIM_MOTOR_FORWARD_SOFT_LIMIT);
        this.aimMotor.setReverseSoftLimit(RobotMap.AIM_MOTOR_REVERSE_SOFT_LIMIT);
        this.aimMotor.enableForwardSoftLimit(true);
        this.aimMotor.enableReverseSoftLimit(true);
        this.aimMotor.ConfigFwdLimitSwitchNormallyOpen(true);
        this.aimMotor.ConfigRevLimitSwitchNormallyOpen(true);
        
        this.aimStick = aimStick;
    }

    @Override
    protected void initDefaultCommand() {
        setDefaultCommand(new SetLauncherHeightCommand(aimStick.getAxis(Joystick.AxisType.kY)));
    }

    // Sets the speed on the flywheels to suck in the boulder
    public void setSpeedIntake() {
        this.intakeLeftMotor.changeControlMode(TalonControlMode.Speed);
        this.intakeRightMotor.changeControlMode(TalonControlMode.Speed);
        this.intakeLeftMotor.set(INTAKE_SPEED);
        this.intakeRightMotor.set(INTAKE_SPEED);
    }

    // Sets the speed on the flywheels to launch the boulder
    public void setSpeedLaunch() {
        this.intakeLeftMotor.changeControlMode(TalonControlMode.Speed);
        this.intakeRightMotor.changeControlMode(TalonControlMode.Speed);
        this.intakeLeftMotor.set(LAUNCH_SPEED);
        this.intakeRightMotor.set(LAUNCH_SPEED);
    }

    // stops the flywheels
    public void setSpeedAbort() {
        this.intakeLeftMotor.changeControlMode(TalonControlMode.Speed);
        this.intakeRightMotor.changeControlMode(TalonControlMode.Speed);
        this.intakeLeftMotor.set(ZERO_SPEED);
        this.intakeRightMotor.set(ZERO_SPEED);
    }

    // moves the launcher, joystick angle determines speed
    public void moveLauncherWithJoystick(double speed) {
        if (!autoAim) {
            if (!launcherBottomSwitch.get() && !launcherTopSwitch.get()) {
                aimMotor.changeControlMode(TalonControlMode.Speed);
                aimMotor.set(speed * JOYSTICK_SCALE);
            } else {
                aimMotor.set(ZERO_SPEED);
            }
        }
    }

    // changes the launcher height by a small value
    // direction is either 1 or -1
    public void incrementLauncherHeight(int direction) {
        if (!autoAim) {
            aimMotor.changeControlMode(TalonControlMode.Position);
            aimMotor.set(aimMotor.getPosition() + (AIM_MOTOR_INCREMENT * direction));
        }
    }

    public void activateLaunchServo() {
        launcherServo.set(LAUNCHER_SERVO_LAUNCH_POSITION);
    }

    public void retractLaunchServo() {
        launcherServo.set(LAUNCHER_SERVO_NEUTRAL_POSITION);
    }

    // toggles auto aim
    // joystick only works while auto aim is off
    public void toggleAutoAim() {
        if (autoAim) {
            autoAim = false;
        } else {
            autoAim = true;
        }
    }

    public void autoAimLauncher() {
            
    }

    public CANTalon getIntakeLeftMotor() {
        return intakeLeftMotor;
    }

    public CANTalon getIntakeRightMotor() {
        return intakeRightMotor;
    }

    public CANTalon getLauncherAimMotor() {
        return aimMotor;
    }

    public DigitalInput getBoulderSwitch() {
        return boulderSwitch;
    }
    
    public boolean getAutoAim() {
        return autoAim;
    }
}
