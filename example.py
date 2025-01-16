import time
from DobotTCP import Dobot, Feedback

robot = Dobot()
feedback = Feedback(robot)
feedback.init()
feedback.get()
print(feedback.data.get("RobotType"))
