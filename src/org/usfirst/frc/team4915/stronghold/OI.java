package org.usfirst.frc.team4915.stronghold;

import java.io.IOException;
import java.io.InputStream;
import java.util.jar.Attributes;
import java.util.jar.Manifest;

import org.usfirst.frc.team4915.stronghold.commands.PortcullisBarIn;
import org.usfirst.frc.team4915.stronghold.commands.PortcullisBarOut;
import org.usfirst.frc.team4915.stronghold.commands.PortcullisBarStop;
import org.usfirst.frc.team4915.stronghold.commands.PortcullisMoveDown;
import org.usfirst.frc.team4915.stronghold.commands.PortcullisMoveUp;
import org.usfirst.frc.team4915.stronghold.commands.DriveTrain.DriveStraightCommand;
import org.usfirst.frc.team4915.stronghold.commands.DriveTrain.ToggleSpeedDown;
import org.usfirst.frc.team4915.stronghold.commands.DriveTrain.ToggleSpeedUp;
import org.usfirst.frc.team4915.stronghold.commands.IntakeLauncher.LightSwitchCommand;
import org.usfirst.frc.team4915.stronghold.commands.IntakeLauncher.Aimer.LauncherGoToPositionCommand;
import org.usfirst.frc.team4915.stronghold.commands.IntakeLauncher.Boulder.IntakeBallCommandGroup;
import org.usfirst.frc.team4915.stronghold.commands.IntakeLauncher.Boulder.LaunchBallCommandGroup;
import org.usfirst.frc.team4915.stronghold.commands.IntakeLauncher.Boulder.SpinIntakeWheelsOutCommand;
import org.usfirst.frc.team4915.stronghold.commands.IntakeLauncher.Boulder.StopWheelsCommand;
import org.usfirst.frc.team4915.stronghold.commands.vision.AutoAimControlCommand;
import org.usfirst.frc.team4915.stronghold.subsystems.Autonomous;
import org.usfirst.frc.team4915.stronghold.vision.robot.VisionState;

import edu.wpi.first.wpilibj.Joystick;
import edu.wpi.first.wpilibj.buttons.JoystickButton;
import edu.wpi.first.wpilibj.command.Command;
import edu.wpi.first.wpilibj.smartdashboard.SendableChooser;
import edu.wpi.first.wpilibj.smartdashboard.SmartDashboard;

/**
 * This class handles the "operator interface", or the interactions between the
 * driver station and the robot code.
 */
public class OI {

    // Ports for joysticks
    public static final int DRIVE_STICK_PORT = 0;
    public static final int LAUNCHER_STICK_PORT = 1;

    // Button numbers for driveStick buttons
    public static final int INTAKE_BALL_BUTTON_NUMBER = 3;
    public static final int DRIVE_STOP_INTAKE_WHEELS_BUTTON_NUMBER = 5;
    public static final int DRIVE_LAUNCHER_JUMP_TO_NEUTRAL_BUTTON_NUMBER = 6;
    public static final int DRIVE_LAUNCHER_JUMP_TO_INTAKE_BUTTON_NUMBER = 4;
    public static final int TURN_SCALER = 8;
    public static final int DRIVE_STRAIGHT_BUTTON_NUMBER = 11; // NB: conflicts with unused shift button


    // Button numbers for launching related buttons on the mechanism stick
    public static final int KICK_BALL_BUTTON_NUMBER = 3;
    public static final int LAUNCHER_NEUTRAL_BUTTON_NUMBER = 8;
    public static final int MECH_STOP_INTAKE_WHEELS_BUTTON_NUMBER = 5;
    public static final int SPIN_INTAKE_WHEELS_OUT_BUTTON_NUMBER = 4;
    public static final int LIGHT_SWITCH_BUTTON_NUMBER = 2;
    public static final int HIGH_LOW_BUTTON_NUMBER = 6;
    public static final int PORTCULLIS_BUTTON_NUMBER_UP = 6;
    public static final int PORTCULLIS_BUTTON_NUMBER_DOWN = 7;
    public static final int PORTCULLIS_BAR_OUT = 11;
    public static final int PORTCULLIS_BAR_IN = 10;
    public static final int PORTCULLIS_BAR_STOP = 9;

    // Create joysticks for driving and aiming the launcher
    public Joystick driveStick;
    public Joystick aimStick;

    // Create buttons for the driveStick
    public JoystickButton speedUpButton;
    public JoystickButton slowDownButton;
    public JoystickButton grabBallButton;
    public JoystickButton driveLauncherJumpToNeutralButton;
    public JoystickButton driveLauncherJumpToIntakeButton;
    public JoystickButton driveStopIntakeWheelsButton;

    // Create buttons for the launcher on the mechanism stick
    public JoystickButton kickBallButton;
    public JoystickButton mechStopWheelsButton;
    public JoystickButton launcherJumpToAngleButton;
    public JoystickButton spinIntakeWheelsOutButton;
    public JoystickButton spinIntakeWheelsOutLowButton;
    public JoystickButton highLowButton;
    public JoystickButton lightSwitchButton;
    public JoystickButton autoLaunchTestButton;
    public JoystickButton launcherNeutralButton;

    // Create buttons for the scaler on the mechanism stick
    public JoystickButton scalerExtendButton;
    public JoystickButton scalerRetractButton;
    public JoystickButton scalerReachUpButton;
    public JoystickButton scalerReachDownButton;
    public JoystickButton scalerLiftButton;
    public JoystickButton speedToggle;
    public JoystickButton driveStraightButton;

    //PORTCULLIS
    public JoystickButton portcullisButtonUp;
    public JoystickButton portcullisButtonDown;
    public JoystickButton portcullisBarIn;
    public JoystickButton portcullisBarOut;
    public JoystickButton portcullisBarStop;
    // variables for the sendable chooser
    public SendableChooser startingFieldPosition;
    public SendableChooser barrierType;
    public SendableChooser strategy;

    public OI() {

        // *****autonomous*****
        // ***Three Sendable Choosers***
        // SendableChooser for the starting field position
        startingFieldPosition = new SendableChooser();
        startingFieldPosition.addDefault("1: Low Bar", Autonomous.Position.ONE);
        startingFieldPosition.addObject("2", Autonomous.Position.TWO);
        startingFieldPosition.addObject("3", Autonomous.Position.THREE);
        startingFieldPosition.addObject("4", Autonomous.Position.FOUR);
        startingFieldPosition.addObject("5", Autonomous.Position.FIVE);
        SmartDashboard.putData("AutoFieldPosition", startingFieldPosition);

        // SendableChooser for the barrier type
        // assigning each barrier to a number
        barrierType = new SendableChooser();
        barrierType.addDefault("Low Bar", Autonomous.Type.LOWBAR);
        barrierType.addObject("Moat", Autonomous.Type.MOAT);
        barrierType.addObject("Rough Terrain", Autonomous.Type.ROUGH_TERRAIN);
        barrierType.addObject("Rock Wall", Autonomous.Type.ROCK_WALL);
        barrierType.addObject("Portcullis ", Autonomous.Type.PORTCULLIS);
        barrierType.addObject("Ramparts", Autonomous.Type.RAMPARTS);
        SmartDashboard.putData("AutoBarrierType", barrierType);

        // SendableChooser for the strategy
        strategy = new SendableChooser();
        strategy.addDefault("None", Autonomous.Strat.DRIVE_ACROSS);
        strategy.addObject("Breach Only", Autonomous.Strat.DRIVE_ACROSS);
        strategy.addObject("Breach, Blind Shot", Autonomous.Strat.DRIVE_SHOOT_NO_VISION);
        strategy.addObject("Breach, Vision Shot", Autonomous.Strat.DRIVE_SHOOT_VISION);
        SmartDashboard.putData("AutoStrategy", strategy);

        this.driveStick = new Joystick(DRIVE_STICK_PORT);
        this.aimStick = new Joystick(LAUNCHER_STICK_PORT);

        // Bind module commands to buttons
        if (ModuleManager.PORTCULLIS_MODULE_ON){
            initializeButton (this.portcullisButtonUp, aimStick, PORTCULLIS_BUTTON_NUMBER_UP, new PortcullisMoveUp());
            initializeButton(this.portcullisButtonDown, aimStick, PORTCULLIS_BUTTON_NUMBER_DOWN, new PortcullisMoveDown());
            initializeButton (this.portcullisBarIn, aimStick, PORTCULLIS_BAR_IN, new PortcullisBarIn());
            initializeButton (this.portcullisBarOut, aimStick, PORTCULLIS_BAR_OUT, new PortcullisBarOut());
            initializeButton (this.portcullisBarStop, aimStick, PORTCULLIS_BAR_STOP, new PortcullisBarStop());
        }

        if (ModuleManager.DRIVE_MODULE_ON) {
	    this.speedToggle = new JoystickButton(driveStick, TURN_SCALER);
	    this.speedToggle.whileHeld(new ToggleSpeedDown());
	    this.speedToggle.whenReleased(new ToggleSpeedUp());

//	    this.driveStraightButton = new JoystickButton(driveStick, DRIVE_STRAIGHT_BUTTON_NUMBER);
//	    this.driveStraightButton.whileHeld(new DriveStraightCommand());
       }

        if (ModuleManager.INTAKELAUNCHER_MODULE_ON) {
            initializeButton(this.kickBallButton, aimStick, KICK_BALL_BUTTON_NUMBER, new LaunchBallCommandGroup());
            initializeButton(this.mechStopWheelsButton, aimStick, MECH_STOP_INTAKE_WHEELS_BUTTON_NUMBER, new StopWheelsCommand());
            initializeButton(this.grabBallButton, driveStick, INTAKE_BALL_BUTTON_NUMBER, new IntakeBallCommandGroup());
            initializeButton(this.spinIntakeWheelsOutButton, aimStick, SPIN_INTAKE_WHEELS_OUT_BUTTON_NUMBER, new SpinIntakeWheelsOutCommand());
            initializeButton(this.driveLauncherJumpToIntakeButton, driveStick, DRIVE_LAUNCHER_JUMP_TO_INTAKE_BUTTON_NUMBER, new LauncherGoToPositionCommand(LauncherGoToPositionCommand.TRAVEL));
            initializeButton(this.driveLauncherJumpToNeutralButton, driveStick, DRIVE_LAUNCHER_JUMP_TO_NEUTRAL_BUTTON_NUMBER, new LauncherGoToPositionCommand(LauncherGoToPositionCommand.NEUTRAL));
            initializeButton(this.driveStopIntakeWheelsButton, driveStick, DRIVE_STOP_INTAKE_WHEELS_BUTTON_NUMBER, new StopWheelsCommand());
            initializeButton(this.driveLauncherJumpToNeutralButton, aimStick, LAUNCHER_NEUTRAL_BUTTON_NUMBER, new LauncherGoToPositionCommand(LauncherGoToPositionCommand.NEUTRAL));
            System.out.println("ModuleManager OI: Initialize IntakeLauncher");
        }

        if (ModuleManager.VISION_MODULE_ON) {
            SmartDashboard.putData(VisionState.getInstance());

            initializeButton(this.highLowButton, aimStick, HIGH_LOW_BUTTON_NUMBER, new AutoAimControlCommand(false, true));
            System.out.println("ModuleManager OI: Initialize Vision!");
        }

        if (ModuleManager.SCALING_MODULE_ON) {
            SmartDashboard.putData("Scaler Winch", RobotMap.scalingWinch);
            SmartDashboard.putData("Scaler Tape Measure Motor", RobotMap.scalingMotor);
            // initializeButton(this.scalerReachUpButton, aimStick,
            // SCALER_REACH_UP_BUTTON_NUMBER, new
            // ScalerCommand(State.REACHING_UP));
            // initializeButton(this.scalerLiftButton, aimStick,
            // SCALER_LIFT_BUTTON_NUMBER, new ScalerCommand(State.LIFTING));
            // initializeButton(this.scalerReachDownButton, aimStick,
            // SCALER_REACH_DOWN_BUTTON_NUMBER, new
            // ScalerCommand(State.REACHING_DOWN));
        }

        if (ModuleManager.IMU_MODULE_ON) {
            // IMU is initialized in RobotMap.java (and reported)
        }

        initializeButton(this.lightSwitchButton, aimStick, LIGHT_SWITCH_BUTTON_NUMBER, new LightSwitchCommand());

        /*
         * VERSION STRING!!
         */
        try (InputStream manifest = getClass().getClassLoader().getResourceAsStream("META-INF/MANIFEST.MF")) {
            Attributes attributes = new Manifest(manifest).getMainAttributes();
            String buildStr = "by: " + attributes.getValue("Built-By") +
    				          "  on: " + attributes.getValue("Built-At") +
    				          "  vers:" + attributes.getValue("Code-Version");
            /* we'd like a single field on the smart dashboard for easier layout/tracking */
            SmartDashboard.putString("Build", buildStr);
            System.out.println("Build " + buildStr);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void initializeButton(JoystickButton Button, Joystick Joystick, int buttonNumber, Command Command) {
        Button = new JoystickButton(Joystick, buttonNumber);
        Button.whenPressed(Command);
    }

    public Joystick getJoystickDrive() {
        return this.driveStick;
    }

    public Joystick getJoystickAimStick() {
        return this.aimStick;
    }
}
