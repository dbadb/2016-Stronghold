package org.usfirst.frc.team4915.stronghold.commands.IntakeLauncher;

import edu.wpi.first.wpilibj.command.Command;
import edu.wpi.first.wpilibj.smartdashboard.SmartDashboard;
import org.usfirst.frc.team4915.stronghold.Robot;
import org.usfirst.frc.team4915.stronghold.subsystems.IntakeLauncher;


public class SpinLaunchWheelsOutCommand extends Command {

    // this command spins the launch wheels outwards so they will launch the
    // ball
	private IntakeLauncher intake;
    public SpinLaunchWheelsOutCommand() {
    	this.intake = Robot.Get().intakeLauncher; 
        requires(this.intake);
    }

    @Override
    protected void initialize() {
        this.intake.setSpeedLaunch();
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

    }

    @Override
    protected void interrupted() {

    }
}
