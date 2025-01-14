import time
from DobotTCP import Dobot, FlexGripper

dobot = Dobot()
gripper = FlexGripper()
dobot.Connect()
dobot.EnableRobot()
dobot.FlexGrip(1)
time.sleep(3)
dobot.FlexGrip(0)