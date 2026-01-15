# SpaceMouse Robot Control Instructions

This program provides a Tkinter-based GUI to control the Dobot Magician robotic arm using a 3Dconnexion **SpaceMouse**, offering fine control of translation, rotation, tool actions, and joint positioning. It supports real-time feedback from the robot and flexible input mapping.

---

## Features

* Real-time SpaceMouse control of the Dobot's position or joints.
* Customizable mapping between SpaceMouse axes and robot joints or Cartesian movement.
* Tool control via SpaceMouse buttons or GUI options (e.g. vacuum suction).
* Joint value entry and GoTo execution.
* Live feedback of actual joint angles and robot status.
* Simulation, Tool, Joints, and Custom control modes.
* Sliders for global speed and movement threshold.
* Translation and rotation locking options.
* Optional status messages for user guidance.

---

## Requirements

* Python 3.8+
* Libraries:

```bash
pip install pyspacemouse tkinter keyboard
```

* A connected and supported 3Dconnexion **SpaceMouse**.
* DobotTCP Python API (must include `Dobot.SetSucker`, `Dobot.MoveJog`, etc.).
* Working USB/serial connection to Dobot Magician.

---

## Setup and Usage

**1. Run the program:**

```bash
python SpaceRobot.py
```

**2. GUI Overview:**

* **Top Row Buttons:**
  Enable / Disable robot, clear errors, home, and emergency STOP.

* **Control Mode:**
  Select between `Simulation`, `Tool`, `Joints`, or `Custom` mode.

* **Mapping Section:**
  Six dropdowns let you assign SpaceMouse inputs (`X`, `Y`, `Z`, `Pitch`, `Roll`, `Yaw`) to joints.
  Indicators next to each combobox light up **red/green** when movement exceeds the threshold.

* **Button Actions:**
  Map SpaceMouse buttons (Left/Right) to actions like "Open Tool", "Close Tool", "User Command".

* **Threshold & Speed Sliders:**
  Adjust the activation threshold (for movement detection) and the global movement speed (1–100).

* **Translation / Rotation Lock:**
  Lock either type of movement via checkboxes.

* **Joint Entry Section:**
  Enter target joint positions (`0.00` to `180.00`) and click **GoTo** to move.
  Click on live joint position labels to copy them to the input fields.

* **Status Bar:**
  Displays system messages, alerts, or connection status

---

## Control Modes

* **Simulation:**
  GUI and movement logic active, but no robot commands are sent.

* **Tool:**
  SpaceMouse controls Cartesian or rotational axes for tool coordinate system.

* **Joints:**
  Each axis maps to a specific robot joint using dropdown assignments.

* **Custom:**
  Full user control. Comboboxes become editable for custom mappings.

---

## How Robot Feedback Works

* Joint angles are fetched continuously in a background thread.
* Actual joint positions are displayed below the input fields.

---

## Input Behavior

* Axis values > threshold highlight green; < -threshold highlight red.
* Corresponding mapped joints/motions are activated once per direction and once when returning to zero.
* SpaceMouse buttons are debounced to trigger once per press.
* User-defined textbox next to Button 1 is only active if "User Command" is selected.

---

## Notes and Tips

* All joint values are validated and clipped between `-180.00` and `180.00`.
* Labels are clickable (e.g., copying actual joint angles to inputs).

---

## Troubleshooting

* Make sure the SpaceMouse is connected and detected (`pyspacemouse.open()` returns True).
* Close any 3D Connexion software
* If feedback is missing, check your Dobot connection.
* If buttons or sliders don’t respond, verify focus is not captured by another widget.
* Restart the application after any disconnection or SpaceMouse driver reload.
