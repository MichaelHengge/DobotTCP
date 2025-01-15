import time
from DobotTCP import Dobot, ServoGripper

robot = Dobot()
gripper = ServoGripper(robot)
robot.Connect()
robot.EnableRobot()
gripper.setState(4)
time.sleep(3)
gripper.setState(1)
