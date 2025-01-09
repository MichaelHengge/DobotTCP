import pyspacemouse
import time
import threading
import tkinter as tk


class SpaceMouseGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SpaceMouse State")

        # Create a canvas for graphical representation
        self.canvas = tk.Canvas(root, width=400, height=500, bg="white")
        self.canvas.pack(pady=20)

        # Draw the SpaceMouse graphic
        self.labels = {}
        self.arrows = {}
        self.axis_labels = {}
        self.buttons = {}
        self.draw_spacemouse()
        self.draw_buttons()

        # Start reading SpaceMouse data in a separate thread
        self.running = True
        self.space_mouse_thread = threading.Thread(target=self.read_spacemouse, daemon=True)
        self.space_mouse_thread.start()

        # Stop button
        self.stop_button = tk.Button(root, text="Stop", command=self.stop)
        self.stop_button.pack(pady=10)

    def draw_spacemouse(self):
        colors = {"X": "blue", "Y": "green", "Z": "red", "Roll": "purple", "Pitch": "orange", "Yaw": "cyan"}

        # Define cube vertices for 3D representation
        front_cube = [(150, 150), (250, 150), (250, 250), (150, 250)]  # Front face
        back_cube = [(120, 120), (220, 120), (220, 220), (120, 220)]   # Back face

        # Draw front face
        self.canvas.create_polygon(front_cube, outline="black", fill="gray", width=2)
        # Draw back face
        self.canvas.create_polygon(back_cube, outline="black", fill="lightgray", width=2)
        # Connect edges
        for i in range(4):
            self.canvas.create_line(front_cube[i][0], front_cube[i][1], back_cube[i][0], back_cube[i][1], fill="black")

        # Draw dynamic axes
        self.arrows["Z"] = self.canvas.create_line(200, 200, 180, 80, arrow="last", fill=colors["Z"], width=2)
        self.labels["Z"] = self.canvas.create_text(160, 50, text="0.0", fill=colors["Z"])
        self.axis_labels["Z"] = self.canvas.create_text(170, 70, text="Z", fill=colors["Z"])

        self.arrows["X"] = self.canvas.create_line(200, 200, 320, 200, arrow="last", fill=colors["X"], width=2)
        self.labels["X"] = self.canvas.create_text(350, 200, text="0.0", fill=colors["X"])
        self.axis_labels["X"] = self.canvas.create_text(330, 190, text="X", fill=colors["X"])

        self.arrows["Y"] = self.canvas.create_line(200, 200, 200, 320, arrow="last", fill=colors["Y"], width=2)
        self.labels["Y"] = self.canvas.create_text(200, 200, text="0.0", fill=colors["Y"])
        self.axis_labels["Y"] = self.canvas.create_text(220, 330, text="Y", fill=colors["Y"])

        # Draw fixed arcs for rotational axes (Roll, Pitch, Yaw) and add labels
        self.canvas.create_arc(100, 100, 300, 300, start=0, extent=90, outline=colors["Roll"], style="arc", width=2)
        self.canvas.create_text(100, 110, text="Roll", fill=colors["Roll"])
        self.labels["Roll"] = self.canvas.create_text(130, 110, text="0.0", fill=colors["Roll"])

        self.canvas.create_arc(140, 140, 280, 280, start=90, extent=90, outline=colors["Pitch"], style="arc", width=2)
        self.canvas.create_text(270, 270, text="Pitch", fill=colors["Pitch"])
        self.labels["Pitch"] = self.canvas.create_text(270, 290, text="0.0", fill=colors["Pitch"])

        self.canvas.create_arc(160, 160, 260, 260, start=180, extent=90, outline=colors["Yaw"], style="arc", width=2)
        self.canvas.create_text(170, 260, text="Yaw", fill=colors["Yaw"])
        self.labels["Yaw"] = self.canvas.create_text(140, 260, text="0.0", fill=colors["Yaw"])

    def draw_buttons(self):
        # Draw representations for two buttons below the axes
        self.buttons["Button1"] = self.canvas.create_rectangle(150, 400, 180, 430, fill="red", outline="black")
        self.buttons["Button2"] = self.canvas.create_rectangle(220, 400, 250, 430, fill="red", outline="black")

        self.canvas.create_text(165, 440, text="Button 1", fill="black")
        self.canvas.create_text(235, 440, text="Button 2", fill="black")

    def read_spacemouse(self):
        success = pyspacemouse.open()
        if success:
            while self.running:
                state = pyspacemouse.read()
                self.update_arrows(state)
                self.update_buttons(state)
                time.sleep(0.005)  # 10 ms delay
        else:
            print("Failed to connect to SpaceMouse")

    def update_arrows(self, state):
        # Map values from -1 to 1 to lengths in the range 50 to 150
        def map_value(value):
            return 100 * abs(value) + 50  # Always positive for length

        # Calculate dynamic arrow lengths
        x_length = map_value(state.x)
        y_length = map_value(state.y)
        z_length = map_value(state.z)

        # Update X-axis arrow
        x_end = 200 + x_length if state.x > 0 else 200 - x_length
        self.canvas.coords(self.arrows["X"], 200, 200, x_end, 200)
        self.canvas.itemconfig(self.labels["X"], text=f"{state.x:.2f}")
        self.canvas.coords(self.labels["X"], x_end + (30 if state.x > 0 else -30), 200)

        # Update Y-axis arrow
        y_end = 200 - y_length if state.y > 0 else 200 + y_length
        self.canvas.coords(self.arrows["Y"], 200, 200, 200, y_end)
        self.canvas.itemconfig(self.labels["Y"], text=f"{state.y:.2f}")
        self.canvas.coords(self.labels["Y"], 200, y_end + (30 if state.y < 0 else -30))

        # Update Z-axis arrow
        z_x_offset = -z_length / 2 if state.z > 0 else z_length / 2
        z_y_offset = -z_length if state.z > 0 else z_length
        self.canvas.coords(self.arrows["Z"], 200, 200, 200 + z_x_offset, 200 + z_y_offset)
        self.canvas.itemconfig(self.labels["Z"], text=f"{state.z:.2f}")
        self.canvas.coords(self.labels["Z"], 200 + z_x_offset - 20, 200 + z_y_offset - 20)

    def update_buttons(self, state):
        # Update button representations based on their states
        button_colors = ["green" if state.buttons[i] else "red" for i in range(2)]
        self.canvas.itemconfig(self.buttons["Button1"], fill=button_colors[0])
        self.canvas.itemconfig(self.buttons["Button2"], fill=button_colors[1])

    def stop(self):
        self.running = False
        self.root.destroy()


# Run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = SpaceMouseGUI(root)
    root.mainloop()
