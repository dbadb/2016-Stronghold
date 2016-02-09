package org.usfirst.frc.team4915.stronghold.commands;

import edu.wpi.first.wpilibj.command.Command;
import org.usfirst.frc.team4915.stronghold.Robot;

public class HighSpeedModeCommand extends Command {

    public HighSpeedModeCommand () {
        requires(Robot.Get().gearShift);
    }
    @Override
    protected void initialize() {
        // switches the gears from low speed to high speed
        // or turns the gears on and goes to high speed mode
        System.out.println("Entering high speed mode");
        Robot.Get().gearShift.highSpeedMode();
        //only uses initializes because the gear only shifts once
    }

    @Override
    protected void execute() {
        // initialize() ran the command - nothing more needed
    }

    @Override
    protected boolean isFinished() {
        return true;
    }

    @Override
    protected void end() {
        // FIXME: call isFinished() to ensure scheduler properly ends/cleans the command
    }

    @Override
    protected void interrupted() {
        // FIXME: call end() to ensure scheduler properly ends/cleans the command
    }

}
