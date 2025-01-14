import time
from Magician import DobotMagicianE6

dobot = DobotMagicianE6()
dobot.Connect()
dobot.EnableRobot()
dobot.DO(2,1)
time.sleep(2)
dobot.DO(2,0)