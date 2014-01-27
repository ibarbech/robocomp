//******************************************************************
// 
//  Generated by IDSL to IDL Translator
//  
//  File name: stewart3L1R.idl
//  Source: stewart3L1R.idsl
//  
//******************************************************************   
#ifndef ROBOCOMPSTEWART3L1R_ICE
#define ROBOCOMPSTEWART3L1R_ICE

#include <JointMotor.ice>

#include <CommonHead.ice>

module RoboCompstewart3L1R{

	interface stewart3L1R{
		RoboCompJointMotor::MotorParamsList getAllMotorParams();
		void  getAllMotorState(out RoboCompJointMotor::MotorStateMap mstateMap);
		void  setPosition(RoboCompJointMotor::MotorGoalPosition goal)throws RoboCompJointMotor::UnknownMotorException, RoboCompJointMotor::HardwareFailedException;
	};
};
  
#endif