import time
from DobotTCP import Dobot, Feedback

robot = Dobot()
robot.Connect()
robot.SetDebugLevel(2)
robot.EnableRobot()

robot.SayBye(20,True)


#robot.Home()
#time.sleep(1)

# pickup hi
'''robot.MoveJJ(285, 0, -135, 45, 90, -104) # above sign
time.sleep(1)
robot.MoveJJ(284, -41.5039, -142.8317, 95.0233, 90, -104) # contact sign
time.sleep(2)
robot.SetSucker(1)
time.sleep(2)
robot.MoveJJ(285, 0, -135, 45, 90, -104) # above sign'''

# pickup bye
'''robot.MoveJJ(122, 0, -135, 45, 90, -104) # above sign
time.sleep(1)
robot.MoveJJ(122, -41.5039, -142.8317, 95.0233, 90, -104) # contact sign
time.sleep(2)
robot.SetSucker(1)
time.sleep(3)
robot.MoveJJ(122, 0, -135, 45, 90, -104) # above sign'''

# Wave
'''robot.MoveJJ(180, 5.6, -52.9, -32.2, 87.8, 11.8)
robot.MoveJJ(180, 5.6, -52.9, 32.2, 87.8, 11.8)
robot.MoveJJ(270, 30, -60, -10, 0, 0)
robot.MoveJJ(270, 60, -30, 30, 0, 0)
robot.MoveJJ(270, 0, -60, -10, 0, 0)
robot.MoveJJ(270, 60, -30, 30, 0, 0)
robot.MoveJJ(270, 0, 0, 0, 0, -30)'''

# Wiggle
#robot.MoveJJ(0, 0, -50, -20, 90, 130)
#robot.MoveJJ(0, 0, -50, 50, 90, 130)
#robot.MoveJJ(90, 0, 50, -50, 0, 130)
#robot.MoveJJ(90, 30, -50, 50, 0, 100)
#robot.MoveJJ(90, 0, 50, -50, 0, 130)
#robot.MoveJJ(90, 30, -50, 50, 0, 100)
#robot.MoveJJ(90, 0, 0, 0, 0, 130)

#time.sleep(25)

# return hi
'''robot.MoveJJ(285, 0, -135, 45, 90, -104) # above sign
time.sleep(1)
robot.MoveJJ(284, -41.5039, -142.8317, 95.0233, 90, -104) # contact sign
time.sleep(2)
robot.SetSucker(0)
time.sleep(2)
robot.MoveJJ(285, 0, -135, 45, 90, -104) # above sign'''

# return bye
'''robot.MoveJJ(122, 0, -135, 45, 90, -104) # above sign
time.sleep(1)
robot.MoveJJ(122, -41.5039, -142.8317, 95.0233, 90, -104) # contact sign
time.sleep(2)
robot.SetSucker(0)
time.sleep(2)
robot.MoveJJ(122, 0, -135, 45, 90, -104) # above sign'''