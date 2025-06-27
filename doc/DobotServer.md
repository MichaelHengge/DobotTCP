# Dobot TCP Flask WebSocket Server

This server exposes a WebSocket interface to control the Dobot robotic arm and its attached grippers (FlexGripper and ServoGripper). It manages incoming commands asynchronously and sends responses back to connected clients.

---

## Features

* Accepts commands via WebSocket `send_command` events.
* Supports Dobot core commands, FlexGripper, and ServoGripper commands.
* Asynchronous command processing with a thread-safe queue.
* Emits command results or errors back to clients.
* Logs client connections and disconnections.
* Configured ping/pong heartbeat to keep WebSocket connections alive.

---

## Requirements

* Python 3.7+
* Flask
* Flask-SocketIO
* DobotTCP library (custom Dobot, FlexGripper, ServoGripper classes)
* Eventlet or gevent (recommended for Flask-SocketIO performance)

Install dependencies with:

```bash
pip install flask flask-socketio eventlet
```

---

## Running the Server

Run the server script:

```bash
python server.py
```

The server listens on:

```html
http://0.0.0.0:5001
```

---

## WebSocket API

### Connect

Clients connect to the WebSocket namespace at:

```
ws://localhost:5001/socket.io/
```

### Events

#### `send_command`

Send commands as JSON with the following format:

```json
{
  "command": "MethodName(arg1, arg2, ...)"
}
```

* `MethodName` can be a Dobot method or one prefixed with `FlexGripper` or `ServoGripper` to target gripper commands.

Example commands:

* `"MoveJog('Z-', 1)"`
* `"FlexGripperSetState(-1)"`
* `"ServoGripperSetState(1)"`

The server queues commands and executes them in order.

#### Responses

* `queued` — emitted when command is queued for execution:

  ```json
  { "command": "MethodName(...)" }
  ```

* `command_response` — emitted after command execution with response or error:

  ```json
  {
    "command": "MethodName(...)",
    "response": "...",
    "error": null
  }
  ```

  or if an error occurred:

  ```json
  {
    "command": "MethodName(...)",
    "error": "Error message"
  }
  ```

---

## Internal Details

* The server runs a background worker thread to process the command queue.
* Commands are parsed by extracting the method name and arguments.
* Based on method name prefix:

  * `FlexGripper*` commands route to the FlexGripper instance.
  * `ServoGripper*` commands route to the ServoGripper instance.
  * All others route to the Dobot robot instance.
* Threading locks protect the shared command queue.
* Ping interval: 25 seconds, Ping timeout: 60 seconds (to maintain WebSocket connection health).

---

## Logs

Client connection and disconnection events are logged to console:

```python
Client connected: <session_id>
Client disconnected: <session_id>
```
