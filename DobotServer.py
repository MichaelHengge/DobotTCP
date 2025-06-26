from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit
from DobotTCP import Dobot, FlexGripper, ServoGripper
import threading
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*", ping_interval=25, ping_timeout=60)

robot = Dobot()
robot.Connect()

flex = FlexGripper(robot)
servo = ServoGripper(robot)

command_queue = []
queue_lock = threading.Lock()

def worker():
    while True:
        cmd = None
        with queue_lock:
            if command_queue:
                cmd = command_queue.pop(0)
        if cmd:
            try:
                func_name = cmd.split("(", 1)[0]
                args_str = cmd[len(func_name)+1:-1]  # Strip parentheses
                args = eval(f"[{args_str}]") if args_str else []

                # Dispatch command based on prefix
                if func_name.startswith("FlexGripper"):
                    flex_method_name = func_name[len("FlexGripper"):]
                    method = getattr(flex, flex_method_name, None)
                elif func_name.startswith("ServoGripper"):
                    servo_method_name = func_name[len("ServoGripper"):]
                    method = getattr(servo, servo_method_name, None)
                else:
                    method = getattr(robot, func_name, None)

                if not method:
                    raise AttributeError(f"Method {func_name} not found on any device")

                response = method(*args)
                socketio.emit('command_response', {
                    'command': cmd,
                    'response': response[1] if isinstance(response, (list, tuple)) and len(response) > 1 else response,
                    'error': response[0] if isinstance(response, (list, tuple)) and len(response) > 0 else None
                })
            except Exception as e:
                socketio.emit('command_response', {
                    'command': cmd,
                    'error': str(e)
                })
            time.sleep(0.02)
        else:
            time.sleep(0.01)

threading.Thread(target=worker, daemon=True).start()

@socketio.on('send_command')
def handle_send_command(json):
    cmd = json.get('command')
    if not cmd:
        emit('error', {'message': 'No command received'})
        return
    with queue_lock:
        command_queue.append(cmd)
    emit('queued', {'command': cmd})

@socketio.on('connect')
def on_connect():
    print(f"Client connected: {request.sid}")

@socketio.on('disconnect')
def on_disconnect():
    print(f"Client disconnected: {request.sid}")

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5001)
