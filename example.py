import time
from DobotTCP import Dobot, Feedback

robot = Dobot()
robot.Connect()
robot.EnableRobot()
robot.Home()
feedback = Feedback(robot)
feedback.Connect()
feedback.Get()
print(feedback.data.get("RobotType"))
