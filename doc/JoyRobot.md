# Joystick Robot Control Instructions

This program provides a joystick-based GUI to control the Dobot robotic arm and its grippers, supporting both direct TCP control and communication via a Flask WebSocket server.

---

## Features

* Uses a physical joystick/gamepad (via pygame) for intuitive robot movement.
* Supports toggling between **direct TCP control** and **Flask server WebSocket control**.
* Visual GUI with button indicators, status messages, and mode toggles.
* Supports controlling different tools attached to the Dobot:

  * Vacuum suction ("sucker")
  * Flex Gripper
  * Servo Gripper
* Automatically manages connection state and reconnects WebSocket client if needed.

---

## Requirements

* Python 3.7+
* Libraries:

```bash
pip install pygame tkinter python-socketio requests
```

* DobotTCP Python API with `Dobot`, `FlexGripper`, and `ServoGripper` classes.
* A joystick/gamepad connected and recognized by the system.
* Flask WebSocket server running on `localhost:5001` (if using server mode).

---

## Setup and Usage

**1. Run the program:**

```bash
python joystick_control.py
```

**2. Joystick Controls:**

* The joystick's axes control robot movement in the X, Y, Z or rotational axes depending on modifier toggle button.
* Buttons are mapped to Z-axis movement and toggling suction/tool control/modifier.
* Modifier button toggles control between cartesian movements and rotation (pitch, roll, yaw).

**3. GUI Elements:**

* Joystick directional indicators light up based on joystick input.
* Suction and modifier indicators show current tool and mode status.
* Status bar at bottom displays current actions and connection states.
* Checkbox toggles between direct TCP and Flask server control modes.

**4. Tool Selection:**

* The variable `current_tool` in the code controls which tool commands are sent.
* Supports `"sucker"`, `"flex"`, and `"servo"` tool modes.
* Modify this variable in code to match your hardware setup.

---

## How Commands Are Sent

* **Direct TCP mode:**
  Commands are called directly on the Dobot API classes.

* **Server mode:**
  Commands are formatted as strings and sent over WebSocket to the Flask server for execution.

---

## Variables to Configure

* `current_tool` — set to `"sucker"`, `"flex"`, or `"servo"` to match your attached tool.
* WebSocket server URL hardcoded as `'http://localhost:5001'` — adjust if server runs elsewhere.

---

## Troubleshooting

* Ensure joystick is connected and detected by pygame (`pygame.joystick.get_count() > 0`).
* Confirm Flask WebSocket server is running if using server mode.
* Use status bar messages to monitor connection state and commands.
* Restart program if joystick or connection issues occur.
* If button mapping is off, unplug and replug joystick and restart program
