import time
from DobotTCP import Dobot, Feedback

robot = Dobot()
robot.Connect()
robot.SetDebugLevel(1)
print(robot.EnableRobot())

robot.MoveJog("J2+")
time.sleep(3)
robot.MoveJog()