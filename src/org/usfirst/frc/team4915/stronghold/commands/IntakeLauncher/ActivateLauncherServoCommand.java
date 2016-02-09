package org.usfirst.frc.team4915.stronghold.commands.IntakeLauncher;

import edu.wpi.first.wpilibj.command.Command;
import org.usfirst.frc.team4915.stronghold.Robot;

public class ActivateLauncherServoCommand extends Command {

    public ActivateLauncherServoCommand() {
        requires(Robot.Get().intakeLauncher);
    }

    protected void initialize() {
        Robot.Get().intakeLauncher.activateLaunchServo();
    }

    protected void execute() {
    
    }

    protected boolean isFinished() {
        return true;
    }

    protected void end() {

    }

    protected void interrupted() {
    
    }
}