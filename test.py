import time
from DobotTCP import Dobot, Feedback

robot = Dobot()
robot.Connect()
robot.SetDebugLevel(2)
robot.EnableRobot()

(_,rsp,_) = robot.GetPose()

print(f"Robot mode: {rsp}")

