# Dobot ControlBox GUI Instructions

This program provides a graphical interface to control a Dobot robotic arm from a serial connection either **directly via TCP** or **via a Flask WebSocket server**.

---

## Features

* Control the Dobot using color-coded buttons with selectable commands.
* Switch between **direct TCP connection** and **Flask WebSocket server** mode.
* Serial monitor window to view incoming serial messages (e.g., from Arduino).
* Automatic buffering and reconnect for WebSocket commands.
* Commands can have parameters (e.g., `MoveJJ` with coordinate tuples).

---

## Requirements

* Python 3.7+
* Required packages:

```bash
pip install pyserial pillow pystray flask-socketio
```

* **Arduino or similar microcontroller** connected to your PC that sends command strings via serial port (e.g., `BUTTON_RED`, `BUTTON_GREEN`), which the GUI interprets as button presses.

---

## Usage

### Starting the Application

Run:

```bash
python controlbox.py
```

### Selecting Control Mode

* **Use Flask Server** checkbox toggles between:

  * **Server Mode:** Sends commands via WebSocket to your Dobot Flask server.
  * **Direct TCP Mode:** Connects directly to the Dobot via TCP.

### Serial Connection

* Select the correct COM port (where your arduino or similar are connected) and baud rate.
* Click **Connect** to open serial connection.
* Use **Refresh** to update available COM ports.

### Using Buttons

* Click colored buttons to send preconfigured commands.
* Select command for each button from the dropdown below it.
* Commands are sent to the Dobot accordingly.

### Serial Monitor

* Displays incoming serial messages from your microcontroller.
* Supports button press emulation from serial input (e.g., `BUTTON_RED` triggers Red button press).

---

## Important Notes

* **Microcontroller Integration:**
  The GUI expects an Arduino or similar device connected via serial port sending text commands that start with `BUTTON_` followed by button color labels (e.g., `BUTTON_RED`). This enables remote physical button control.

* **WebSocket Mode:**
  When using the Flask server, commands are sent as JSON over a persistent WebSocket connection. The GUI buffers one command if the connection is temporarily down and sends it on reconnect.

---

## Adding Commands

You can customize the commands your ControlBox GUI sends to the Dobot by editing the `COMMAND_OPTIONS` list near the top of the code.

### Location in Code

```python
COMMAND_OPTIONS = [
    ("None", None),
    ("Clear Error", "ClearError"),
    ("Place", ("MoveJJ", (9, -47, -70, 26, 91, -2))),
    ("Welcom", ("SayHi", (20, True))),
    ("Say Hi!", "SayHi"),
    ("Say Bye", "SayBye"),
    # Add your commands here
]
```

---

### Command Format

Each command is a tuple consisting of:

* **Label (string):**
  The  name displayed in the dropdown menu below each button.

* **Command (string or tuple):**

  * **String:** Name of the method to call with no parameters.
    Example: `"ClearError"` calls `robot.ClearError()`.
  * **Tuple:** A tuple where the first element is the method name (string), and the second element is a tuple of arguments.
    Example: `("MoveJJ", (9, -47, -70, 26, 91, -2))` calls `robot.MoveJJ(9, -47, -70, 26, 91, -2)`.

---

### Adding a New Command Example

Suppose you want to add a command to move to coordinates `(100, 200, 150)` with the method `MoveTo`.

Add this entry:

```python
("Move To Position", ("MoveTo", (100, 200, 150)))
```

---

### How Commands Are Sent

* If the GUI is in **direct TCP mode**, the program calls the corresponding Dobot method directly with parameters.
* If in **Flask server mode**, the command is sent as a formatted string over WebSocket, e.g.:

  * `MoveJJ(9, -47, -70, 26, 91, -2)`
  * `ClearError()`

The server parses and executes these commands on the robot.

---

## Troubleshooting

* Ensure your microcontroller is correctly sending button commands if using serial mode.
* Confirm the Flask server is running and reachable at `http://localhost:5001` if using server mode.
* Use the **Serial Monitor** to debug incoming serial data.
* Restart the app if COM ports are not detected, or use the Refresh button.