
package org.usfirst.frc.team4915.stronghold;

import edu.wpi.first.wpilibj.IterativeRobot;
import edu.wpi.first.wpilibj.DriverStation;
import edu.wpi.first.wpilibj.command.Command;
import edu.wpi.first.wpilibj.command.Scheduler;
import edu.wpi.first.wpilibj.livewindow.LiveWindow;
import edu.wpi.first.wpilibj.smartdashboard.SmartDashboard;
import org.usfirst.frc.team4915.stronghold.commands.MoveStraightPositionModeCommand;
import org.usfirst.frc.team4915.stronghold.subsystems.DriveTrain;
import org.usfirst.frc.team4915.stronghold.subsystems.GearShift;
import org.usfirst.frc.team4915.stronghold.subsystems.IntakeLauncher;

import java.util.Arrays;

/**
 * The VM is configured to automatically run this class, and to call the
 * functions corresponding to each mode, as described in the IterativeRobot
 * documentation. If you change the name of this class or the package after
 * creating this project, you must also update the manifest file in the resource
 * directory.
 */
public class Robot extends IterativeRobot {
	
	// Get is shorthand/alias for getInstance()
	public static Robot Get() {
		return getInstance();
	}

	public synchronized static Robot getInstance() {
		if (s_instance == null)
			s_instance = new Robot();
		return s_instance;
	}

	private static Robot s_instance;
	
    public DriveTrain driveTrain;
    public IntakeLauncher intakeLauncher;
    public OI oi;
    public GearShift gearShift;
    public Command autonomousCommand;
    
    /**
     * This function is run when the robot is first started up and should be
     * used for any initialization code.
     */
    @Override
    public void robotInit() {    	
    	// 1. initialize operator interface... subsystems want access to Joystick,
    	try {
    		this.oi = new OI();
            this.reportInitSuccess("OI");
    	}
    	catch(Throwable t) {
        	this.reportInitFailure("OI", t);
    	}
        // 2. conditionally create the modules
        try  {
            this.driveTrain = new DriveTrain(this.oi.driveStick);
            this.gearShift = new GearShift();
            this.reportInitSuccess("DriveTrain");
        }
        catch (Throwable t) {
        	this.reportInitFailure("DriveTrain", t);
        }
        try {
            this.intakeLauncher = new IntakeLauncher(this.oi.aimStick);
            this.reportInitSuccess("IntakeLauncher");
        }
        catch (Throwable t) {
        	this.reportInitFailure("IntakeLauncher", t);
        }
    }

    @Override
    public void disabledPeriodic() {
        Scheduler.getInstance().run();
    }

    @Override
    public void autonomousInit() {
        // schedule the autonomous command
        autonomousCommand = new MoveStraightPositionModeCommand(30);    // in inches
        if (this.autonomousCommand != null) {
            this.autonomousCommand.start();
        }
    }

    /**
     * This function is called periodically during autonomous
     */
    @Override
    public void autonomousPeriodic() {
        Scheduler.getInstance().run();
    }

    @Override
    public void teleopInit() {
        // This makes sure that the autonomous stops running when
        // teleop starts running. If you want the autonomous to
        // continue until interrupted by another command, remove
        // this line or comment it out.
        if (this.autonomousCommand != null) {
            this.autonomousCommand.cancel();
        }
    }

    /**
     * This function is called when the disabled button is hit. You can use it
     * to reset subsystems before shutting down.
     */
    @Override
    public void disabledInit() {

    }

    /**
     * This function is called periodically during operator control
     */
    @Override
    public void teleopPeriodic() {
        Scheduler.getInstance().run();
    }

    /**
     * This function is called periodically during test mode
     */
    @Override
    public void testPeriodic() {
        LiveWindow.run();
    }
    
    private void reportInitSuccess(String subsystem) {
        SmartDashboard.putString(subsystem, "Initialized");
        System.out.println(subsystem + ": Initialized");
    }
    
    private void reportInitFailure(String subsystem, Throwable t) {
    	SmartDashboard.putString(subsystem, "BORKED");
    	DriverStation.reportError(subsystem +
                "Init ERROR - unhandled exception: " + t.toString() + " at "
                    + Arrays.toString(t.getStackTrace()), false); 

    }

}
