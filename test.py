import time
from DobotTCP import Dobot, Feedback

robot = Dobot()
robot.Connect()
robot.SetDebugLevel(1)
feedback = Feedback(robot)
feedback.Connect()

'''feedback.Get()
mode = feedback.data.get('RobotMode')
print("Fetching robot feedback: ", mode)

time.sleep(1)
'''

robot.EnableRobot()

robot.MoveJJ(-90, -40, -80, 30, 90, 0)
robot.DO(1, 1)
robot.DO(2, 1)
robot.MovL("joint={-90, 0, -80, 30, 90, 0}")
time.sleep(2000)
robot.MovL("joint={-90, -40, -80, 30, 90, 0}")
robot.DO(1, 0)
robot.DO(2, 0)
robot.MoveJJ(-90, 0, -80, 30, 90, 0)
