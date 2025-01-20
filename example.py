import time
from DobotTCP import Dobot, Feedback

robot = Dobot()
robot.Connect()

(err, rsp, cmd) = robot.EnableRobot()
print(f"  Error code: {err}")
print(f"  Response: {rsp}")
print(f"  Command: {cmd}")


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