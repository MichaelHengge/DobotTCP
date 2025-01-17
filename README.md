# DobotTCP Library

DobotTCP is a Python library to control the Dobot  robot range via its TCP interface. The library provides functions for managing motion, I/O, and configuration of the Dobot robot. It was specially developed with the Dobot MagicianE6 in mind.

<p align="center">
<a href="https://hits.seeyoufarm.com"><img src="https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2FMichaelHengge%2FDobotTCP&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false"/></a>
<img src="https://img.shields.io/github/license/MichaelHengge/DObotTCP?style=flat-square">
<img src="https://img.shields.io/github/stars/MichaelHengge/DObotTCP?style=flat-square">
<img src="https://img.shields.io/github/forks/MichaelHengge/DObotTCP?style=flat-square">
<img src="https://img.shields.io/github/issues/MichaelHengge/DObotTCP?style=flat-square">
<a href="https://www.pepy.tech/projects/DObotTCP" target="_blank"><img src="https://static.pepy.tech/badge/DObotTCP"></a>
</p>

## Installation

Install the library via pip:

```bash
pip install DobotTCP
```

Ensure Python 3.6+ is installed. Install dependencies if not automatically installed:

```bash
pip install multipledispatch
```

Import the library in your project:

```python
from DobotTCP import Dobot
```

## Basic Usage

### Example

```python
from DobotTCP import Dobot

# COnnect and enable the robot
robot = Dobot(ip="192.168.5.1", port=29999)
robot.Connect()
robot.EnableRobot()

# Move robot with joint motion to pose
MovJ("pose={200,200,200,0,0,0}")

# Home robot
robot.Home()

robot.Disconnect()
```

## Included Classes

Addidtional classes for robot accessories have been added

### Flexible Gripper

Basic controls for a flexible gripper

```python
from DobotTCP import Dobot, FlexGripper

robot = Dobot()
gripper = FlexGripper(robot)
gripper.Open()
gripper.Close()
```

### Servo Gripper

Basic controls for a servo gripper (IO mode)

```python
from DobotTCP import Dobot, ServoGripper

robot = Dobot()
servo_gripper = ServoGripper(robot)
servo_gripper.SetState(1)  # Open
servo_gripper.SetState(2)  # Close
```

### Feedback

This class was implemented to receive feedback from the robot via TCP.

```python
from DobotTCP import Dobot, Feedback

robot = Dobot()
feedback = Feedback(robot)
feedback.Connect()
feedback.Get()
print(feedback.data.get("RobotType"))
```

## Notes

- This class was written with the intention to stay as close to the syntax formatting of the original Dobot TCP protocol. Therefore, not all python style guids are followed. For example function names start with a capital letter.

- Since method overloading is not trivial in python, some functions had to be changed in order to make them work in python. This is especially the case for the tray functions.

## Contributing

Feel free to contribute to the project by submitting issues or pull requests.

## License

This project is licensed under the MIT License.
