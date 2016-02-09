package org.usfirst.frc.team4915.stronghold.commands.IntakeLauncher;

import edu.wpi.first.wpilibj.command.Command;
import org.usfirst.frc.team4915.stronghold.Robot;

public class RetractLauncherServoCommand extends Command {

    public RetractLauncherServoCommand() {
        requires(Robot.Get().intakeLauncher);
    }

    protected void initialize() {
        Robot.Get().intakeLauncher.retractLaunchServo();
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
