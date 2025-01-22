import threading
import tkinter as tk
from tkinter import StringVar, ttk, Canvas
import pyspacemouse
import time

from DobotTCP import Dobot

class SpaceMouseGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SpaceMouse Control GUI")
        self.root.geometry("500x630")
        self.toolState = 0
        self.initialized = False
        self.isEnabled = False
        self.robotMode = -1
        self.motionMode = ""
        self.mode = tk.StringVar(value="Simulation")
        self.axis_states = {  # Track axis activity states
            "X": "inactive",
            "Y": "inactive",
            "Z": "inactive",
            "Pitch": "inactive",
            "Roll": "inactive",
            "Yaw": "inactive",
        }

        # Variables to store SpaceMouse data
        self.axis_data = [0, 0, 0]
        self.rotation_data = [0, 0, 0]  # Pitch, Roll, Yaw
        self.button_data = "Button 0: Released, Button 1: Released"

        # Add top button row
        top_button_frame = tk.Frame(self.root)
        top_button_frame.pack(fill="x", pady=10)

        button_container = tk.Frame(top_button_frame)
        button_container.pack(anchor="center")  # Center the buttons

        self.enable_button = tk.Button(button_container, text="Enable", bg="green", fg="white", command=self.on_enable)
        self.enable_button.pack(side=tk.LEFT, padx=5)

        clear_error_button = tk.Button(button_container, text="Clear Error", command=self.on_clear_error)
        clear_error_button.pack(side=tk.LEFT, padx=5)

        home_button = tk.Button(button_container, text="Home", command=self.on_home)
        home_button.pack(side=tk.LEFT, padx=5)

        stop_button = tk.Button(button_container, text="EMERGENCY STOP", command=self.on_stop, bg="red", fg="white")
        stop_button.pack(side=tk.LEFT, padx=5)

        # Threshold slider
        self.threshold = tk.DoubleVar(value=0.5)
        slider_frame = tk.Frame(self.root)
        slider_frame.pack(pady=10)

        tk.Label(slider_frame, text="Threshold:").pack(side=tk.LEFT, padx=5)
        threshold_slider = ttk.Scale(slider_frame, from_=0.1, to=1.0, orient="horizontal", variable=self.threshold)
        threshold_slider.pack(side=tk.LEFT, padx=5)
        threshold_value_label = tk.Label(slider_frame, textvariable=self.threshold, width=4)
        threshold_value_label.pack(side=tk.LEFT, padx=5)

        self.threshold.trace("w", self.update_threshold_display)
        self.mode.trace("w", self.update_combobox_options)

        # Mode switch radio buttons
        mode_frame = tk.Frame(self.root)
        mode_frame.pack(pady=10)

        tk.Label(mode_frame, text="Mode:").pack(side=tk.LEFT, padx=5)

        simulation_radio = tk.Radiobutton(mode_frame, text="Simulation", variable=self.mode, value="Simulation")
        simulation_radio.pack(side=tk.LEFT, padx=5)

        joints_radio = tk.Radiobutton(mode_frame, text="Joints", variable=self.mode, value="Joints")
        joints_radio.pack(side=tk.LEFT, padx=5)

        user_radio = tk.Radiobutton(mode_frame, text="User", variable=self.mode, value="User")
        user_radio.pack(side=tk.LEFT, padx=5)

        tool_radio = tk.Radiobutton(mode_frame, text="Tool", variable=self.mode, value="Tool")
        tool_radio.pack(side=tk.LEFT, padx=5)

        # Lock controls checkboxes
        self.lock_translation = tk.BooleanVar(value=False)  # Default: unlocked
        self.lock_rotation = tk.BooleanVar(value=False)  # Default: unlocked

        lock_controls_frame = tk.Frame(self.root)
        lock_controls_frame.pack(pady=10)

        translation_checkbox = tk.Checkbutton(lock_controls_frame, text="Lock Translation", variable=self.lock_translation)
        translation_checkbox.pack(side=tk.LEFT, padx=5)

        rotation_checkbox = tk.Checkbutton(lock_controls_frame, text="Lock Rotation", variable=self.lock_rotation)
        rotation_checkbox.pack(side=tk.LEFT, padx=5)


        # Add horizontal separator
        separator = ttk.Separator(self.root, orient="horizontal")
        separator.pack(fill="x", pady=5)

        # Comboboxes for joint mapping
        self.mapping_labels = []
        self.comboboxes = []
        self.indicators = []

        mapping_frame = tk.Frame(self.root)
        mapping_frame.pack(pady=20)

        tk.Label(mapping_frame, text="Map SpaceMouse inputs to robot joints:").pack(pady=(0, 10))

        labels = ["X", "Y", "Z", "Roll", "Pitch", "Yaw"]
        preselected_values = ["Joint 1", "Joint 2", "Joint 3", "Joint 4", "Joint 5", "Joint 6"]  # Default for "Joints" mode

        for i, label_text in enumerate(labels):
            # Create a row frame for consistent alignment
            row_frame = tk.Frame(mapping_frame)
            row_frame.pack(fill="x", pady=5)  # Fill horizontally for alignment

            # Add label
            label = tk.Label(row_frame, text=f"{label_text}:", width=10, anchor="w")
            label.pack(side=tk.LEFT, padx=5)
            self.mapping_labels.append(label)

            # Add combobox
            combobox = ttk.Combobox(row_frame, state="readonly", width=15)
            combobox["values"] = preselected_values  # Set initial options
            combobox.set(preselected_values[i])  # Preselect default value
            combobox.pack(side=tk.LEFT, padx=5)
            self.comboboxes.append(combobox)

            # Add indicator
            canvas = Canvas(row_frame, width=20, height=20, highlightthickness=0)
            circle = canvas.create_oval(2, 2, 18, 18, outline="black", fill="white")
            canvas.pack(side=tk.LEFT, padx=5)
            self.indicators.append((canvas, circle))

        # Add comboboxes for button mapping
        button_mapping_frame = tk.Frame(self.root)
        button_mapping_frame.pack(pady=20)

        tk.Label(button_mapping_frame, text="Map SpaceMouse buttons to robot actions:").pack(pady=(0, 10))

        button_options = ["None", "Toggle Tool", "Home", "Pack", "Pickup", "Toggle Mode"]
        button_actions = ["Button L", "Button R"]
        preselected_buttons = ["Toggle Tool", "Pickup"]
        self.button_indicators = []

        for i, button in enumerate(button_actions):
            frame = tk.Frame(button_mapping_frame)
            frame.pack(pady=5)

            label = tk.Label(frame, text=f"{button}:")
            label.pack(side=tk.LEFT, padx=5)

            combobox = ttk.Combobox(frame, values=button_options, state="readonly")
            combobox.set(preselected_buttons[i])
            combobox.pack(side=tk.LEFT, padx=5)
            self.comboboxes.append(combobox)

            canvas = Canvas(frame, width=20, height=20, highlightthickness=0)
            circle = canvas.create_oval(2, 2, 18, 18, outline="black", fill="white")
            canvas.pack(side=tk.LEFT, padx=5)
            self.button_indicators.append((canvas, circle))

        # Track button press states
        self.button_states = {"Button 0": False, "Button 1": False}

        # Add a legend for the indicators
        legend_frame = tk.Frame(self.root)
        legend_frame.pack(pady=20)

        tk.Label(legend_frame, text="Indicator Legend:").pack(pady=(0, 10))

        sample_frame = tk.Frame(legend_frame)
        sample_frame.pack()

        # Sample for green
        green_canvas = Canvas(sample_frame, width=20, height=20, highlightthickness=0)
        green_canvas.create_oval(2, 2, 18, 18, outline="black", fill="green")
        green_canvas.pack(side=tk.LEFT, padx=5)
        tk.Label(sample_frame, text="Positive (> Threshold)").pack(side=tk.LEFT, padx=10)

        # Sample for red
        red_canvas = Canvas(sample_frame, width=20, height=20, highlightthickness=0)
        red_canvas.create_oval(2, 2, 18, 18, outline="black", fill="red")
        red_canvas.pack(side=tk.LEFT, padx=5)
        tk.Label(sample_frame, text="Negative (< -Threshold)").pack(side=tk.LEFT, padx=10)

        # Sample for white
        white_canvas = Canvas(sample_frame, width=20, height=20, highlightthickness=0)
        white_canvas.create_oval(2, 2, 18, 18, outline="black", fill="white")
        white_canvas.pack(side=tk.LEFT, padx=5)
        tk.Label(sample_frame, text="Neutral").pack(side=tk.LEFT, padx=10)

        # Running flag for thread
        self.running = True

        # Start SpaceMouse thread
        self.spacemouse_thread = threading.Thread(target=self.read_spacemouse)
        self.spacemouse_thread.daemon = True
        self.spacemouse_thread.start()

        # Start GUI update loop
        self.update_gui()

    def update_threshold_display(self, *args):
        """Limit the threshold display to two decimal places."""
        self.threshold.set(round(self.threshold.get(), 2))

    def update_combobox_options(self, *args):
        """Update combobox options and preselect values based on the selected mode."""
        if self.mode.get() == "Joints":
            options = ["Joint 1", "Joint 2", "Joint 3", "Joint 4", "Joint 5", "Joint 6"]
            preselected_values = options
        else:  # Tool mode
            options = ["X", "Y", "Z", "Rx", "Ry", "Rz"]
            preselected_values = options

        for i, combobox in enumerate(self.comboboxes[:6]):
            combobox["values"] = options  # Update the options
            combobox.set(preselected_values[i])  # Reset the preselected value

    def read_spacemouse(self):
        """Read data from the SpaceMouse."""
        success = pyspacemouse.open()
        if success:
            while self.running:
                state = pyspacemouse.read()
                self.axis_data = [state.x, state.y, state.z]
                self.rotation_data = [state.pitch, state.roll, state.yaw]
                self.button_data = (
                    f"Button 0: {'Pressed' if state.buttons[0] else 'Released'}, "
                    f"Button 1: {'Pressed' if state.buttons[1] else 'Released'}"
                )
                time.sleep(0.005)  # 10 ms delay
        else:
            print("Failed to connect to SpaceMouse")

    def update_indicator(self, canvas, circle, value):
        """Update the color of an indicator based on the value."""
        threshold = self.threshold.get()
        color = "green" if value > threshold else "red" if value < -threshold else "white"
        canvas.itemconfig(circle, fill=color)

    def on_translation_x_active(self, direction):
        mode = self.mode.get()
        if mode == "Joints":
            if direction == "positive":
                robot.MoveJog("J1-")
            elif direction == "negative":
                robot.MoveJog("J1+")
            elif direction == "zero":
                robot.MoveJog()
        elif mode == "Tool" or mode == 'User':  # Tool or User mode
            mID = 1 if mode == "User" else 2
            if direction == "positive":
                robot.MoveJog("X+", mID)
            elif direction == "negative":
                robot.MoveJog("X-", mID)
            elif direction == "zero":
                robot.MoveJog()

    def on_translation_y_active(self, direction):
        mode = self.mode.get()
        if mode == "Joints":
            if direction == "positive":
                robot.MoveJog("J2+")
            elif direction == "negative":
                robot.MoveJog("J2-")
            elif direction == "zero":
                robot.MoveJog()
        elif mode == "Tool" or mode == 'User':  # Tool or User mode
            mID = 1 if mode == "User" else 2
            if direction == "positive":
                robot.MoveJog("Y-", mID)
            elif direction == "negative":
                robot.MoveJog("Y+", mID)
            elif direction == "zero":
                robot.MoveJog()
 
    def on_translation_z_active(self, direction):
        mode = self.mode.get()
        if mode == "Joints":
            if direction == "positive":
                robot.MoveJog("J3-")
            elif direction == "negative":
                robot.MoveJog("J3+")
            elif direction == "zero":
                robot.MoveJog()
        elif mode == "Tool" or mode == 'User':  # Tool or User mode
            mID = 1 if mode == "User" else 2
            if direction == "positive":
                robot.MoveJog("Z-", mID)
            elif direction == "negative":
                robot.MoveJog("Z+", mID)
            elif direction == "zero":
                robot.MoveJog()

    def on_rotation_pitch_active(self, direction):
        mode = self.mode.get()
        if mode == "Joints":
            if direction == "positive":
                robot.MoveJog("J4+")
            elif direction == "negative":
                robot.MoveJog("J4-")
            elif direction == "zero":
                robot.MoveJog()
        elif mode == "Tool" or mode == 'User':  # Tool or User mode
            mID = 1 if mode == "User" else 2
            if direction == "positive":
                robot.MoveJog("Rx+", mID)
            elif direction == "negative":
                robot.MoveJog("Rx-", mID)
            elif direction == "zero":
                robot.MoveJog()

    def on_rotation_roll_active(self, direction):
        mode = self.mode.get()
        if mode == "Joints":
            if direction == "positive":
                robot.MoveJog("J5+")
            elif direction == "negative":
                robot.MoveJog("J5-")
            elif direction == "zero":
                robot.MoveJog()
        elif mode == "Tool" or mode == 'User':  # Tool or User mode
            mID = 1 if mode == "User" else 2
            if direction == "positive":
                robot.MoveJog("Ry+", mID)
            elif direction == "negative":
                robot.MoveJog("Ry-", mID)
            elif direction == "zero":
                robot.MoveJog()

    def on_rotation_yaw_active(self, direction):
        mode = self.mode.get()
        if mode == "Joints":
            if direction == "positive":
                robot.MoveJog("J6+")
            elif direction == "negative":
                robot.MoveJog("J6-")
            elif direction == "zero":
                robot.MoveJog()
        elif mode == "Tool" or mode == 'User':  # Tool or User mode
            mID = 1 if mode == "User" else 2
            if direction == "positive":
                robot.MoveJog("Rz+", mID)
            elif direction == "negative":
                robot.MoveJog("Rz-", mID)
            elif direction == "zero":
                robot.MoveJog()

    def on_button_0_pressed(self):
        selected_value = self.comboboxes[6].get()
        print(f"Button 0 pressed. Selected action: {selected_value}")
        match selected_value:
            case "Toggle Tool":
                if self.toolState == 0:
                    robot.SetSucker(1)
                    self.toolState = 1
                else:
                    robot.SetSucker(0)
                    self.toolState = 0
            case "Home":
                robot.Home()
            case "Pack":
                robot.Pack()
            case "Pickup":
                robot.MoveJJ(48,34,83,-26,-90,0)
            case "Toggle Mode":
                self.motionMode = self.mode.get()
                pass

    def on_button_1_pressed(self):
        selected_value = self.comboboxes[7].get()
        print(f"Button 0 pressed. Selected action: {selected_value}")
        match selected_value:
            case "Toggle Tool":
                if self.toolState == 0:
                    robot.SetSucker(1)
                    self.toolState = 1
                else:
                    robot.SetSucker(0)
                    self.toolState = 0
            case "Home":
                robot.Home()
            case "Pack":
                robot.Pack()
            case "Pickup":
                robot.MoveJJ(48,34,83,-26,-90,0)
            case "Toggle Mode":
                self.motionMode = self.mode.get()
                pass

    def update_gui(self):
        """Update the GUI with the latest SpaceMouse data."""
        values = self.axis_data + self.rotation_data
        axis_names = ["X", "Y", "Z", "Pitch", "Roll", "Yaw"]

        for i, (value, axis_name) in enumerate(zip(values, axis_names)):
            if (axis_name in ["X", "Y", "Z"] and self.lock_translation.get()) or (axis_name in ["Roll", "Pitch", "Yaw"] and self.lock_rotation.get()):
                continue  # Skip locked movements
            self.update_indicator(self.indicators[i][0], self.indicators[i][1], value)  # Update indicators

            # Get current threshold
            threshold = self.threshold.get()

            # Handle state transitions
            if abs(value) > threshold:  # Above threshold
                if self.axis_states[axis_name] != "active":
                    self.axis_states[axis_name] = "active"  # Mark as active
                    direction = "positive" if value > 0 else "negative"
                    if axis_name == "X":
                        self.on_translation_x_active(direction)
                    elif axis_name == "Y":
                        self.on_translation_y_active(direction)
                    elif axis_name == "Z":
                        self.on_translation_z_active(direction)
                    elif axis_name == "Pitch":
                        self.on_rotation_pitch_active(direction)
                    elif axis_name == "Roll":
                        self.on_rotation_roll_active(direction)
                    elif axis_name == "Yaw":
                        self.on_rotation_yaw_active(direction)

            elif abs(value) <= threshold:  # Zero or below threshold
                if self.axis_states[axis_name] == "active":  # Only trigger zero if previously active
                    self.axis_states[axis_name] = "zero"  # Mark as zero
                    if axis_name == "X":
                        self.on_translation_x_active("zero")
                    elif axis_name == "Y":
                        self.on_translation_y_active("zero")
                    elif axis_name == "Z":
                        self.on_translation_z_active("zero")
                    elif axis_name == "Pitch":
                        self.on_rotation_pitch_active("zero")
                    elif axis_name == "Roll":
                        self.on_rotation_roll_active("zero")
                    elif axis_name == "Yaw":
                        self.on_rotation_yaw_active("zero")

        button_states = self.button_data.split(", ")
        for i, (canvas, circle) in enumerate(self.button_indicators):
            is_pressed = "Pressed" in button_states[i] if i < len(button_states) else False
            color = "green" if is_pressed else "white"
            canvas.itemconfig(circle, fill=color)

            # Debouncing logic
            button_name = f"Button {i}"
            if is_pressed and not self.button_states[button_name]:
                self.button_states[button_name] = True  # Update state
                if i == 0:
                    self.on_button_0_pressed()
                elif i == 1:
                    self.on_button_1_pressed()
            elif not is_pressed:
                self.button_states[button_name] = False  # Reset state when released

        if not self.initialized:
            self.initialized = True

        # Schedule the next update
        self.root.after(50, self.update_gui)

    def stop(self):
        """Stop the SpaceMouse thread."""
        self.running = False

    def on_enable(self):
        print(f"State: {self.isEnabled}")
        if self.isEnabled:
            print("Disabling robot.")
            self.enable_button.config(text="Enable")
            self.isEnabled = False
            robot.DisableRobot()
        else:
            print("Enabling robot.")
            self.enable_button.config(text="Disable")
            self.isEnabled = True
            robot.EnableRobot()

    def on_clear_error(self):
        robot.ClearError()

    def on_home(self):
        robot.Home()

    def on_stop(self):
        print("STOP button pressed.")
        robot.EmergencyStop(1)

if __name__ == "__main__":
    global robotMode
    root = tk.Tk()
    app = SpaceMouseGUI(root)
    robot = Dobot()

    # Ensure clean exit
    def on_closing():
        app.stop()
        root.destroy()

    robot.Connect()
    robot.SetDebugLevel(0)
    (_,robotMode,_) = robot.RobotMode()

    if robotMode == "{4}": # Disabled
        app.enable_button.config(text="Enable")
        app.isEnabled = False
    elif robotMode == "{5}": # Enabled
        app.enable_button.config(text="Disable")
        app.isEnabled = True
    else:
        print(f"Unknown robot mode ({robotMode}).")


    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
