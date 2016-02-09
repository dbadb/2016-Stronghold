package org.usfirst.frc.team4915.stronghold.commands.IntakeLauncher;

import edu.wpi.first.wpilibj.command.Command;
import edu.wpi.first.wpilibj.smartdashboard.SmartDashboard;
import org.usfirst.frc.team4915.stronghold.subsystems.IntakeLauncher;
import org.usfirst.frc.team4915.stronghold.Robot;

public class IntakeBallCommand extends Command {
	
	private IntakeLauncher intake;

    // this command spins the intake flywheels inward to retrieve the ball
    public IntakeBallCommand() {
    	this.intake = Robot.Get().intakeLauncher; 
        requires(this.intake);
    }

    @Override
    protected void initialize() {
        this.intake.setSpeedIntake();
    }

    @Override
    protected void execute() {
        //reports the speed of the motor as it increases
        SmartDashboard.putString("Intake Flywheels", 
        						"Right: " + Double.toString(this.intake.getIntakeRightMotor().getSpeed()) + 
        						" Left: " + Double.toString(this.intake.getIntakeLeftMotor().getSpeed()));
    }

    @Override
    protected boolean isFinished() {
        // ends once the ball is in the basket and presses the limit switch
        SmartDashboard.putBoolean("Boulder in Basket", this.intake.boulderSwitch.get());
        return this.intake.boulderSwitch.get();
    }

    @Override
    protected void end() {

    }

    @Override
    protected void interrupted() {
        
    }
}
