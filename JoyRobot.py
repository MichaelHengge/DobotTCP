import pygame
import tkinter as tk
from DobotTCP import Dobot, FlexGripper, ServoGripper
import threading
import time
import requests
import socketio #pip install "python-socketio[client]"

# Global Variables
suction_on = False
suction_debounced = False
modifier_on = False
modifier_debounced = False
stop_sent = False

robot = None
flex = None
servo = None

current_tool = "flex"  # "sucker" or "flex", "servo"
flex_state = 0  # start at neutral

# Initialize pygame
pygame.init()
pygame.joystick.init()

sio = socketio.Client(
    reconnection=True,
    reconnection_attempts=5,      # Retry a few times only
    reconnection_delay=1,         # 1 second between retries
    reconnection_delay_max=3,     # Max 3 seconds delay
    randomization_factor=0.1      # Small jitter to avoid sync issues
)

def set_status(message):
    root.after(0, lambda: status_var.set(message))

@sio.event
def connect():
    set_status("WebSocket connected")

@sio.event
def disconnect():
    set_status("WebSocket disconnected")

@sio.event
def reconnect():
    set_status("WebSocket reconnecting...")

@sio.on('queued')
def on_queued(data):
    # You could update status here if desired
    pass

@sio.on('command_response')
def on_command_response(data):
    # Optionally show command responses
    # set_status(f"Cmd: {data.get('command')} Response: {data.get('response')}")
    pass


def is_server_running(url="http://localhost:5001"):
    try:
        r = requests.get(url, timeout=1)
        return r.status_code == 200 or r.status_code == 404  # 404 OK if root not defined
    except Exception:
        return False

def connect_ws():
    while True:
        try:
            if not sio.connected:
                sio.connect('http://localhost:5001')
            # Stay connected — wait here while connected
            while sio.connected:
                time.sleep(1)
        except Exception as e:
            set_status(f"WS connect failed: {e}")
            time.sleep(3)  # wait a bit before retrying

def on_toggle_mode():
    global robot, servo, flex
    if use_server.get():
        set_status("Switched to Flask server mode")
        # Disconnect robot TCP connection if active
        if robot:
            try:
                robot.Disconnect()
            except Exception:
                pass
            robot = None
        # Connect Socket.IO client if not connected
        if not sio.connected:
            threading.Thread(target=connect_ws, daemon=True).start()
    else:
        set_status("Switched to direct TCP mode")
        # Disconnect Socket.IO client if connected
        if sio.connected:
            sio.disconnect()
        # Connect to robot via TCP if not connected
        if robot is None:
            robot = Dobot()
            flex = FlexGripper(robot)
            servo = ServoGripper(robot)
            try:
                robot.Connect()
                robot.SetDebugLevel(2)
                robot.EnableRobot()
            except Exception as e:
                set_status(f"Robot connection failed: {e}")

# GUI setup
root = tk.Tk()
root.title("Joystick Robot Control")
root.geometry("400x500")
root.configure(bg="black")
canvas = tk.Canvas(root, width=400, height=500, bg="black", highlightthickness=0)
use_server = tk.BooleanVar(value=True)
toggle = tk.Checkbutton(root, text="Use Flask Server", variable=use_server, command=on_toggle_mode, bg="black", fg="white", selectcolor="black")
toggle.pack(pady=5)

status_var = tk.StringVar(value="Ready")
status_label = tk.Label(root, textvariable=status_var, bg="black", fg="white", font=("Arial", 12))
status_label.pack(side="bottom", fill="x")
status_label.pack(side="bottom", fill="x")

canvas.pack()

# Initialize robot

if not use_server.get():
    robot = Dobot()
    robot.Connect()
    robot.SetDebugLevel(2)
    robot.EnableRobot()
    flex = FlexGripper(robot)
    servo = ServoGripper(robot)

# Top buttons (1 and 2)
circle_radius = 30
button_positions = [(120, 80), (280, 80)]
buttons = []
for x, y in button_positions:
    btn = canvas.create_oval(x - circle_radius, y - circle_radius, x + circle_radius, y + circle_radius, fill="gray")
    buttons.append(btn)

# Button labels
button1_label = canvas.create_text(120, 80, text="Z-", fill="white", font=("Arial", 16, "bold"))
button2_label = canvas.create_text(280, 80, text="Z+", fill="white", font=("Arial", 16, "bold"))

# Parameters for triangle size/placement
center_x, center_y = 200, 280
triangle_height = 100    
triangle_base = 60
label_offset = 12

# Parameter for sub-triangle
sub_triangle_base_half = circle_radius / 2
sub_triangle_height = circle_radius /2

sub_triangle_top_x = 120 + sub_triangle_base_half
sub_triangle_top_y = 80 + circle_radius * 2

mod_triangle_top_x = 280 - sub_triangle_base_half
mod_triangle_top_y = 80 + circle_radius * 2

# Calculate triangle points
triangles = {
    "DOWN": canvas.create_polygon(
        center_x, center_y - triangle_height,
        center_x - triangle_base//2, center_y - triangle_height + triangle_base,
        center_x + triangle_base//2, center_y - triangle_height + triangle_base,
        fill="gray"
    ),
    "UP": canvas.create_polygon(
        center_x, center_y + triangle_height,
        center_x - triangle_base//2, center_y + triangle_height - triangle_base,
        center_x + triangle_base//2, center_y + triangle_height - triangle_base,
        fill="gray"
    ),
    "LEFT": canvas.create_polygon(
        center_x - triangle_height, center_y,
        center_x - triangle_height + triangle_base, center_y - triangle_base//2,
        center_x - triangle_height + triangle_base, center_y + triangle_base//2,
        fill="gray"
    ),
    "RIGHT": canvas.create_polygon(
        center_x + triangle_height, center_y,
        center_x + triangle_height - triangle_base, center_y - triangle_base//2,
        center_x + triangle_height - triangle_base, center_y + triangle_base//2,
        fill="gray"
    ),
    "SUCTION": canvas.create_polygon(
        sub_triangle_top_x - sub_triangle_base_half, sub_triangle_top_y,      # left
        sub_triangle_top_x + sub_triangle_base_half, sub_triangle_top_y,      # right
        sub_triangle_top_x - sub_triangle_base_half, sub_triangle_top_y + sub_triangle_height * 2,         # tip
        fill="gray"
    ),
    "MODIFIER": canvas.create_polygon(
        mod_triangle_top_x - sub_triangle_base_half, mod_triangle_top_y,           # left base
        mod_triangle_top_x + sub_triangle_base_half, mod_triangle_top_y,           # right base
        mod_triangle_top_x + sub_triangle_base_half, mod_triangle_top_y + sub_triangle_height * 2,              # tip
        fill="gray"
    )
}

# Direction Labels
down_label = canvas.create_text(
    center_x, 
    center_y - triangle_height + triangle_base//2 + label_offset, 
    text="Y+", fill="white", font=("Arial", 14, "bold")
)
up_label = canvas.create_text(
    center_x, 
    center_y + triangle_height - triangle_base//2 - label_offset, 
    text="Y-", fill="white", font=("Arial", 14, "bold")
)
left_label = canvas.create_text(
    center_x - triangle_height + triangle_base//2 + label_offset, 
    center_y, 
    text="X-", fill="white", font=("Arial", 14, "bold")
)
right_label = canvas.create_text(
    center_x + triangle_height - triangle_base//2 - label_offset, 
    center_y, 
    text="X+", fill="white", font=("Arial", 14, "bold")
)
# SUCTION triangle (already correct)
suction_left_x = sub_triangle_top_x - sub_triangle_base_half
suction_right_x = sub_triangle_top_x + sub_triangle_base_half
suction_tip_x = sub_triangle_top_x
suction_base_y = sub_triangle_top_y
suction_tip_y = sub_triangle_top_y + sub_triangle_height * 2

suction_centroid_x = (suction_left_x + suction_right_x + suction_tip_x) / 3
suction_centroid_y = (suction_base_y + suction_base_y + suction_tip_y) / 3

suction_label = canvas.create_text(
    suction_centroid_x*0.94, suction_centroid_y,
    text="S", fill="white", font=("Arial", 12, "bold")
)

# MODIFIER triangle (corrected)
mod_left_x = mod_triangle_top_x - sub_triangle_base_half
mod_right_x = mod_triangle_top_x + sub_triangle_base_half
mod_tip_x = mod_triangle_top_x
mod_base_y = mod_triangle_top_y
mod_tip_y = mod_triangle_top_y + sub_triangle_height * 2

mod_centroid_x = (mod_left_x + mod_right_x + mod_tip_x) / 3
mod_centroid_y = (mod_base_y + mod_base_y + mod_tip_y) / 3

mod_label = canvas.create_text(
    mod_centroid_x*1.02, mod_centroid_y,
    text="M", fill="white", font=("Arial", 12, "bold")
)

def send_via_server(command):
    try:
        sio.emit('send_command', {'command': command})
    except Exception as e:
        set_status(f"[WS ERROR] {e}")

    
def move_jog(axis=None, coord_type=None):
    if use_server.get():
        if axis is None:
            send_via_server("MoveJog()")
        elif coord_type is not None:
            send_via_server(f"MoveJog('{axis}', {coord_type})")
        else:
            send_via_server(f"MoveJog('{axis}')")
    else:
        if axis is None:
            robot.MoveJog()
        elif coord_type is not None:
            robot.MoveJog(axis, coord_type)
        else:
            robot.MoveJog(axis)

def set_tool(suction_on):
    global flex_state
    if current_tool == "sucker":
        if use_server.get():
            send_via_server(f"SetSucker({int(suction_on)})")
        else:
            robot.SetSucker(int(suction_on))
    elif current_tool == "flex":
        flex_state = 1 if suction_on else -1
        if use_server.get():
            send_via_server(f"FlexGripperSetState({flex_state})")
        else:
            flex.SetState(flex_state)
    elif current_tool == "servo":
        servo_state = 1 if suction_on else 0  # or adjust depending on your servo states
        if use_server.get():
            send_via_server(f"servo.SetState({servo_state})")
        else:
            servo.SetState(servo_state)
    else:
        print(f"Unknown tool: {current_tool}")


def update_labels():
    if modifier_on:
        canvas.itemconfig(button1_label, text="Rz+")
        canvas.itemconfig(button2_label, text="Rz-")
        canvas.itemconfig(left_label,  text="Rx-")
        canvas.itemconfig(right_label, text="Rx+")
        canvas.itemconfig(up_label,    text="Ry-")
        canvas.itemconfig(down_label,  text="Ry+")
    else:
        canvas.itemconfig(button1_label, text="Z-")
        canvas.itemconfig(button2_label, text="Z+")
        canvas.itemconfig(left_label,  text="X-")
        canvas.itemconfig(right_label, text="X+")
        canvas.itemconfig(up_label,    text="Y-")
        canvas.itemconfig(down_label,  text="Y+")

def joystick_robot_control():
    global suction_on, suction_debounced, modifier_on, modifier_debounced, stop_sent
    while True:
        pygame.event.pump()
        if pygame.joystick.get_count() > 0:
            js = pygame.joystick.Joystick(0)
            move_x = js.get_axis(0)  # X Axis
            move_y = js.get_axis(1)  # Y Axis
            btn1 = js.get_button(0)  # Z down
            btn2 = js.get_button(1)  # Z up
            btn3 = js.get_button(2)  # Suction toggle
            btn4 = js.get_button(3)  # Modifier

            # GUI feedback (unchanged)
            canvas.itemconfig(triangles["LEFT"], fill="red" if move_x < 0 else "gray")
            canvas.itemconfig(triangles["RIGHT"], fill="red" if move_x > 0 else "gray")
            canvas.itemconfig(triangles["DOWN"], fill="red" if move_y < 0 else "gray")
            canvas.itemconfig(triangles["UP"], fill="red" if move_y > 0 else "gray")
            canvas.itemconfig(buttons[0], fill="red" if btn1 else "gray")
            canvas.itemconfig(buttons[1], fill="red" if btn2 else "gray")
            canvas.itemconfig(triangles["SUCTION"], fill="green" if suction_on else "gray")
            canvas.itemconfig(triangles["MODIFIER"], fill="green" if modifier_on else "gray")

            if not modifier_on:
                # Default: cartesian XY + Z
                if btn1:
                    move_jog("Z-", 1)
                    set_status("Moving down")
                    stop_sent = False
                elif btn2:
                    move_jog("Z+", 1)
                    set_status("Moving up")
                    stop_sent = False
                elif move_x != 0 or move_y != 0:
                    if abs(move_x) > abs(move_y):
                        if move_x > 0:
                            move_jog("Y+", 1)
                            set_status("Moving right")
                            stop_sent = False
                        else:
                            move_jog("Y-", 1)
                            set_status("Moving left")
                            stop_sent = False
                    else:
                        if move_y > 0:
                            move_jog("X+", 1)
                            set_status("Moving back")
                            stop_sent = False
                        else:
                            move_jog("X-", 1)
                            set_status("Moving front")
                            stop_sent = False
                else:
                    if not stop_sent:
                        move_jog()  # Stop movement
                        set_status("Ready")
                        stop_sent = True
            else:
                # Modifier ON: Pitch, Roll, Yaw
                if btn1:
                    move_jog("Rz+", 1)
                    set_status("Changing Yaw positive")
                    stop_sent = False
                elif btn2:
                    move_jog("Rz-", 1)
                    set_status("Changing Yaw positive")
                    stop_sent = False
                elif move_x != 0 or move_y != 0:
                    if abs(move_x) > abs(move_y):
                        # X axis controls Pitch
                        if move_x > 0:
                            move_jog("Rx+", 1)
                            set_status("Changing Pitch positive")
                            stop_sent = False
                        else:
                            move_jog("Rx-", 1)
                            set_status("Changing Pitch negative")
                            stop_sent = False
                    else:
                        # Y axis controls Roll
                        if move_y > 0:
                            move_jog("Ry+", 1)
                            set_status("Changing Roll positive")
                            stop_sent = False
                        else:
                            move_jog("Ry-", 1)
                            set_status("Changing Roll negative")
                            stop_sent = False
                else:
                    if not stop_sent:
                        move_jog()  # Stop movement
                        set_status("Ready")
                        stop_sent = True

            # Suction toggle
            if btn3 and not suction_debounced:
                suction_on = not suction_on
                if (suction_on):
                    set_tool(1)
                    set_status("Suction off")
                else:
                    set_tool(0)
                    set_status("Suction on")
                suction_debounced = True
            elif not btn3:
                suction_debounced = False

            # Modifier toggle
            if btn4 and not modifier_debounced:
                modifier_on = not modifier_on
                modifier_debounced = True
                update_labels()
            elif not btn4:
                modifier_debounced = False

        time.sleep(0.05)

# Start robot control thread
threading.Thread(target=connect_ws, daemon=True).start()
threading.Thread(target=joystick_robot_control, daemon=True).start()

# Tkinter loop
root.mainloop()
