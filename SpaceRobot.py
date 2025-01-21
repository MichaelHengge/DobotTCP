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
        self.root.geometry("500x620")
        self.toolState = 0

        # Variables to store SpaceMouse data
        self.axis_data = [0, 0, 0]
        self.rotation_data = [0, 0, 0]  # Pitch, Roll, Yaw
        self.button_data = "Button 0: Released, Button 1: Released"

        # StringVars for GUI labels
        self.axis_var = StringVar()
        self.axis_var.set("Translation: X: 0, Y: 0, Z: 0")

        self.rotation_var = StringVar()
        self.rotation_var.set("Rotation: Pitch: 0, Roll: 0, Yaw: 0")

        self.button_var = StringVar()
        self.button_var.set("Buttons: None pressed")

        # Create and place labels
        self.axis_label = tk.Label(self.root, textvariable=self.axis_var)
        self.axis_label.pack(pady=5)

        self.rotation_label = tk.Label(self.root, textvariable=self.rotation_var)
        self.rotation_label.pack(pady=5)

        self.button_label = tk.Label(self.root, textvariable=self.button_var)
        self.button_label.pack(pady=5)

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

        # Add horizontal separator
        separator = ttk.Separator(self.root, orient="horizontal")
        separator.pack(fill="x", pady=10)

        # Comboboxes for joint mapping
        self.mapping_labels = []
        self.comboboxes = []
        self.indicators = []

        mapping_frame = tk.Frame(self.root)
        mapping_frame.pack(pady=20)

        tk.Label(mapping_frame, text="Map SpaceMouse inputs to robot joints:").pack()

        spacemouse_values = ["None", "X", "Y", "Z", "Pitch", "Roll", "Yaw"]
        robot_joints = ["Joint 1", "Joint 2", "Joint 3", "Joint 4", "Joint 5", "Joint 6"]
        preselected_values = ["X", "Y", "Z", "Pitch", "Roll", "Yaw"]

        for i, joint in enumerate(robot_joints):
            frame = tk.Frame(mapping_frame)
            frame.pack(pady=5)

            label = tk.Label(frame, text=f"{joint}:")
            label.pack(side=tk.LEFT, padx=5)
            self.mapping_labels.append(label)

            combobox = ttk.Combobox(frame, values=spacemouse_values, state="readonly")
            combobox.set(preselected_values[i])
            combobox.pack(side=tk.LEFT, padx=5)
            self.comboboxes.append(combobox)

            canvas = Canvas(frame, width=20, height=20, highlightthickness=0)
            circle = canvas.create_oval(2, 2, 18, 18, outline="black", fill="white")
            canvas.pack(side=tk.LEFT, padx=5)
            self.indicators.append((canvas, circle))

        # Add comboboxes for button mapping
        button_mapping_frame = tk.Frame(self.root)
        button_mapping_frame.pack(pady=20)

        tk.Label(button_mapping_frame, text="Map SpaceMouse buttons to robot actions:").pack()

        button_options = ["None", "Toggle Tool", "Home", "Pack"]
        button_actions = ["Button 0", "Button 1"]
        preselected_buttons = ["Toggle Tool", "Home"]
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

        tk.Label(legend_frame, text="Indicator Legend:").pack()

        sample_frame = tk.Frame(legend_frame)
        sample_frame.pack()

        # Sample for green
        green_canvas = Canvas(sample_frame, width=20, height=20, highlightthickness=0)
        green_canvas.create_oval(2, 2, 18, 18, outline="black", fill="green")
        green_canvas.pack(side=tk.LEFT, padx=5)
        tk.Label(sample_frame, text="Active (> Threshold)").pack(side=tk.LEFT, padx=10)

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
        pass

    def on_translation_y_active(self, direction):
        pass

    def on_translation_z_active(self, direction):
        pass

    def on_rotation_pitch_active(self, direction):
        pass

    def on_rotation_roll_active(self, direction):
        pass

    def on_rotation_yaw_active(self, direction):
        pass

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

    def on_button_1_pressed(self):
        selected_value = self.comboboxes[7].get()
        print(f"Button 1 pressed. Selected action: {selected_value}")
        match selected_value:
            case "Home":
                robot.Home()
            case "Pack":
                robot.Pack()

    def update_gui(self):
        """Update the GUI with the latest SpaceMouse data."""
        values = self.axis_data + self.rotation_data

        for i, (canvas, circle) in enumerate(self.indicators):
            self.update_indicator(canvas, circle, values[i])
            if i == 0 and abs(values[i]) > self.threshold.get():
                self.on_translation_x_active("positive" if values[i] > self.threshold.get() else "negative")
            elif i == 1 and abs(values[i]) > self.threshold.get():
                self.on_translation_y_active("positive" if values[i] > self.threshold.get() else "negative")
            elif i == 2 and abs(values[i]) > self.threshold.get():
                self.on_translation_z_active("positive" if values[i] > self.threshold.get() else "negative")
            elif i == 3 and abs(values[i]) > self.threshold.get():
                self.on_rotation_pitch_active("positive" if values[i] > self.threshold.get() else "negative")
            elif i == 4 and abs(values[i]) > self.threshold.get():
                self.on_rotation_roll_active("positive" if values[i] > self.threshold.get() else "negative")
            elif i == 5 and abs(values[i]) > self.threshold.get():
                self.on_rotation_yaw_active("positive" if values[i] > self.threshold.get() else "negative")

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

        self.axis_var.set(f"Translation: X: {self.axis_data[0]:.2f}, Y: {self.axis_data[1]:.2f}, Z: {self.axis_data[2]:.2f}")
        self.rotation_var.set(f"Rotation: Pitch: {self.rotation_data[0]:.2f}, Roll: {self.rotation_data[1]:.2f}, Yaw: {self.rotation_data[2]:.2f}")
        self.button_var.set(f"Buttons: {self.button_data}")

        # Schedule the next update
        self.root.after(50, self.update_gui)

    def stop(self):
        """Stop the SpaceMouse thread."""
        self.running = False

if __name__ == "__main__":
    root = tk.Tk()
    app = SpaceMouseGUI(root)
    robot = Dobot()

    # Ensure clean exit
    def on_closing():
        app.stop()
        root.destroy()

    robot.Connect()
    robot.SetDebugLevel(0)
    robot.EnableRobot()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
