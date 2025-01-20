import time
from DobotTCP import Dobot, Feedback

robot = Dobot()
robot.Connect()
resp = robot.EnableRobot()
print(f"Response: {resp}")



'''
robot.Pack()
feedback = Feedback(robot)
feedback.Connect()
feedback.Get()
mode = feedback.data.get('RobotMode')
print(robot.ParseRobotMode(mode))

for key, value in feedback.data.items():
    print(f"{key}: {value}")

'''