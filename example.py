from DobotTCP import Dobot, Feedback

robot = Dobot()
robot.Connect()
robot.SetDebugLevel(1)

(err, rsp, cmd) = robot.EnableRobot()
print(f"  Error code: {err}")
print(f"  Response: {rsp}")
print(f"  Command: {cmd}")

robot.Home()

feedback = Feedback(robot)
feedback.Connect()
feedback.Get()
mode = feedback.data.get('RobotMode')
print(robot.ParseRobotMode(mode))

for key, value in feedback.data.items():
    print(f"{key}: {value}")

res = robot.RelJointMovJ(100.0,0.0,0.0,0.0,0.0,0.0)
print(res)

#robot.Disconnect()