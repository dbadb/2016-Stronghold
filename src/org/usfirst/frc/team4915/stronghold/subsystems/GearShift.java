package org.usfirst.frc.team4915.stronghold.subsystems;

import edu.wpi.first.wpilibj.DoubleSolenoid;
import edu.wpi.first.wpilibj.command.Subsystem;
import edu.wpi.first.wpilibj.smartdashboard.SmartDashboard;

import org.usfirst.frc.team4915.stronghold.RobotMap;
import org.usfirst.frc.team4915.stronghold.commands.HighSpeedModeCommand;
import org.usfirst.frc.team4915.stronghold.commands.LowSpeedModeCommand;


public class GearShift extends Subsystem {
    
	public DoubleSolenoid doubleSolenoid;
	
	public GearShift()
	{
        // TODO: Invert motors here if needed: someMotor.setInverted(true)
        this.doubleSolenoid = new DoubleSolenoid(RobotMap.SOLENOID_CHANNEL_PRIMARY, 
        										 RobotMap.SOLENOID_CHANNEL_SECONDARY);
	}

    @Override
    protected void initDefaultCommand() {
        // TODO Auto-generated method stub
    }
    
    /*
     * switches the gears from low speed to high speed
     * or turns the gears on and goes to high speed mode
     */
    public void highSpeedMode() {
        SmartDashboard.putString("Gear", "high");         
        doubleSolenoid.set(DoubleSolenoid.Value.kForward);
    }
    
    /*
     * switches the gears from high speed to low speed
     * or turns the gears on and goes to low speed mode
     */
    public void lowSpeedMode() {
        SmartDashboard.putString("Gear", "low");         
        doubleSolenoid.set(DoubleSolenoid.Value.kReverse);
    }

}
