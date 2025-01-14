import time
from Magician import DobotMagicianE6

dobot = DobotMagicianE6()
dobot.Connect()
dobot.EnableRobot()
dobot.FlexGrip(1)
time.sleep(3)
dobot.FlexGrip(0)