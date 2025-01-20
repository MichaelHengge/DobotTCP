import time
from DobotTCP import Dobot, Feedback

robot = Dobot()
robot.Connect()
robot.EnableRobot()
robot.Home()
feedback = Feedback(robot)
feedback.init()
feedback.get()
print(feedback.data.get("RobotType"))
