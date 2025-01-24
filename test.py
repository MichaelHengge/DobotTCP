import time
from DobotTCP import Dobot, Feedback

robot = Dobot()
robot.Connect()
robot.SetDebugLevel(1)
feedback = Feedback(robot)
feedback.Connect()

feedback.Get()
mode = feedback.data.get('RobotMode')
print("Fetching robot feedback: ", mode)

time.sleep(1)

robot.EnableRobot()
feedback.Get()
mode = feedback.data.get('RobotMode')
print("Fetching robot feedback: ", mode)
