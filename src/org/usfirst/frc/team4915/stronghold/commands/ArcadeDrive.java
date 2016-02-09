
package org.usfirst.frc.team4915.stronghold.commands;

import edu.wpi.first.wpilibj.Joystick;
import edu.wpi.first.wpilibj.command.Command;
import org.usfirst.frc.team4915.stronghold.subsystems.DriveTrain;

public class ArcadeDrive extends Command {

    private Joystick joystickDrive;
    private DriveTrain driveTrain;
    private double joystickX;
    private double joystickY;
    private double joystickZ;

    public ArcadeDrive(Joystick driveStick, DriveTrain driveTrain) {
        // Use requires() here to declare subsystem dependencies
    	this.driveTrain = driveTrain;
        requires(this.driveTrain);
    	this.joystickDrive = driveStick;
    }

    // Called just before this Command runs the first time
    @Override
    protected void initialize() {
    }

    // Called repeatedly when this Command is scheduled to run
    @Override
    protected void execute() {

        this.joystickX = this.joystickDrive.getAxis(Joystick.AxisType.kX);
        this.joystickY = this.joystickDrive.getAxis(Joystick.AxisType.kY);
        this.joystickZ = this.joystickDrive.getAxis(Joystick.AxisType.kZ);

        this.driveTrain.joystickThrottle = this.driveTrain.modifyThrottle();
        // checks where the joystick is
        if ((Math.abs(this.joystickX) < Math.abs(0.075)) && (Math.abs(this.joystickY) < Math.abs(0.075))) {

            if (Math.abs(this.joystickZ) < Math.abs(0.075)) {
                // all in the middle (x,y,z), stops
                this.driveTrain.stop();
            }
            // x and y is in middle but z is twisted
            else {
                this.driveTrain.twistDrive(this.joystickDrive);
            }
        } else {
        	this.driveTrain.arcadeDrive(this.joystickDrive);
        }
    }

    // Make this return true when this Command no longer needs to run execute()
    @Override
    protected boolean isFinished() {
        return false;
    }

    // Called once after isFinished returns true
    @Override
    protected void end() {
    }

    // Called when another command which requires one or more of the same
    // subsystems is scheduled to run
    @Override
    protected void interrupted() {
    }

}
