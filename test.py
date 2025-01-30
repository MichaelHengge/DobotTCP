import time
from DobotTCP import Dobot, Feedback

robot = Dobot()
robot.Connect()
robot.SetDebugLevel(2)
robot.EnableRobot()

rsp = robot.GetAngle()

print(rsp)

