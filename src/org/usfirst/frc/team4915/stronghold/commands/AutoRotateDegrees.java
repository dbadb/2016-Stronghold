package org.usfirst.frc.team4915.stronghold.commands;

import edu.wpi.first.wpilibj.RobotDrive;
import edu.wpi.first.wpilibj.command.Command;
import org.usfirst.frc.team4915.stronghold.Robot;
import org.usfirst.frc.team4915.stronghold.subsystems.DriveTrain;

public class AutoRotateDegrees extends Command {
	private DriveTrain driveTrain;
    private RobotDrive robotDrive;
    private boolean goLeft;
    double robotAngle;

    // autonomous rotate command
    public AutoRotateDegrees(boolean left, double robotAngle) {
    	this.driveTrain = Robot.Get().driveTrain;
    	this.robotDrive = this.driveTrain.robotDrive;
        this.goLeft = left;
        this.robotAngle = robotAngle;
        requires(this.driveTrain);
    }

    @Override
    protected void initialize() {
        // TODO Auto-generated method stub
        this.driveTrain.calibrateGyro();
    }

    @Override
    protected void execute() {
        // TODO Auto-generated method stub
    	this.driveTrain.turn(goLeft);
    }

    @Override
    protected boolean isFinished() {
        // TODO Auto-generated method stub
        return (Math.abs(this.driveTrain.trackGyro()) >= robotAngle);
    }

    @Override
    protected void end() {
        // TODO Auto-generated method stub
        this.robotDrive.stopMotor();
    }

    @Override
    protected void interrupted() {
        // TODO Auto-generated method stub
        end();

    }

}
