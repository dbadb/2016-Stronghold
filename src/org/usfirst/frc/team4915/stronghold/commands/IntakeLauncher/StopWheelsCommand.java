package org.usfirst.frc.team4915.stronghold.commands.IntakeLauncher;

import edu.wpi.first.wpilibj.command.Command;
import edu.wpi.first.wpilibj.smartdashboard.SmartDashboard;
import org.usfirst.frc.team4915.stronghold.Robot;
import org.usfirst.frc.team4915.stronghold.subsystems.IntakeLauncher;

public class StopWheelsCommand extends Command {

    // this command stops the intake flywheels
	private IntakeLauncher intake;
    public StopWheelsCommand() {
    	this.intake = Robot.Get().intakeLauncher;
        requires(this.intake);
    }

    @Override
    protected void initialize() {
        this.intake.setSpeedAbort();
    }

    @Override
    protected void execute() {
        SmartDashboard.putString("Intake Flywheels", 
        				"Right: " + Double.toString(this.intake.getIntakeRightMotor().getSpeed()) + 
        				" Left: " + Double.toString(this.intake.getIntakeLeftMotor().getSpeed()));
    }

    @Override
    protected boolean isFinished() {
        return true;
    }

    @Override
    protected void end() {
        isFinished();
    }

    @Override
    protected void interrupted() {

    }

}
