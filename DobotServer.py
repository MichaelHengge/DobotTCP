from flask import Flask, request, jsonify
from DobotTCP import Dobot, FlexGripper, ServoGripper

app = Flask(__name__)
robot = Dobot()
robot.Connect()

flex = FlexGripper(robot)
servo = ServoGripper(robot)

@app.route("/send", methods=["POST"])
def send_command():
    data = request.json
    command = data.get("command", "")

    if not command:
        return jsonify({"error": "Missing command"}), 400

    try:
        # Parse function name and args
        func_name = command.split("(", 1)[0]
        args_str = command[len(func_name)+1:-1]  # Strip outer parentheses
        args = eval(f"[{args_str}]") if args_str else []

        method = getattr(robot, func_name)
        response = method(*args)
        return jsonify({
            "command": command,
            "response": response[1],
            "error": response[0]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/disconnect", methods=["POST"])
def disconnect():
    robot.Disconnect()
    return jsonify({"status": "Disconnected"})

@app.route("/gripper/flex", methods=["POST"])
def flex_gripper():
    action = request.json.get("action")
    if action == "open":
        return jsonify(flex.Open())
    elif action == "close":
        return jsonify(flex.Close())
    elif action == "neutral":
        return jsonify(flex.Neutral())
    else:
        return jsonify({"error": "Invalid action"}), 400

@app.route("/gripper/flex/state", methods=["POST"])
def flex_gripper_state():
    state = int(request.json.get("state", 0))  # -1, 0, or 1
    return jsonify(flex.SetState(state))

@app.route("/gripper/servo", methods=["POST"])
def servo_gripper():
    state = int(request.json.get("state", 1))  # 1-4
    return jsonify(servo.SetState(state))

@app.route("/gripper/servo/status", methods=["GET"])
def servo_status():
    return jsonify({"status": servo.GetState()})

@app.route("/suction", methods=["POST"])
def suction_control():
    status = int(request.json.get("status", 0))  # 0 = OFF, 1 = ON
    return jsonify(robot.ToolDO(1, status))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
