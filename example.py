import time
from DobotTCP import Dobot, Feedback

robot = Dobot()
robot.Connect()
robot.EnableRobot()
robot.Pack()
feedback = Feedback(robot)
feedback.Connect()
feedback.Get()
mode = feedback.data.get('RobotMode')
print(robot.ParseRobotMode(mode))
'''
for key, value in feedback.data.items():
    print(f"{key}: {value}")
'''
