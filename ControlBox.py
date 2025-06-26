import time
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageDraw, ImageTk, ImageEnhance
import serial.tools.list_ports  # pip install pyserial
import pystray
import threading
import sys
import serial
from DobotTCP import Dobot
import socketio

BUTTONS = [
    ("RED", "#FF0000"),
    ("YELLOW", "#FFFF00"),
    ("GREEN", "#00FF00"),
    ("BLUE", "#0000FF"),
    ("BLACK", "#333333")
]

COMMAND_OPTIONS = [
    ("None", None),
    ("Clear Error", "ClearError"),
    ("Place", ("MoveJJ", (9, -47, -70, 26, 91, -2))),
    ("Welcom", ("SayHi", (20, True))), 
    ("Say Hi!", "SayHi"), 
    ("Say Bye", "SayBye"), 
    # ("Move To Position", ("MoveJJ", (100, 200, 150)))  # Example with parameters
]

GUI_SIZE = "900x250"
GUI_EXTENDED = "900x600"
BUTTON_SIZE = 90
BORDER_SIZE = 10

class ControlPanel(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Dobot Control Panel")
        self.configure(bg="#efefef")
        self.geometry(GUI_SIZE)
        self.resizable(False, False)
        self.expanded = False

        self.use_server = tk.BooleanVar(value=True)
        self.robot = None

        # Socket.IO client
        self.sio = socketio.Client(
            reconnection=True,
            reconnection_attempts=5,      # Retry a few times only
            reconnection_delay=1,         # 1 second between retries
            reconnection_delay_max=3,     # Max 3 seconds delay
            randomization_factor=0.1      # Small jitter to avoid sync issues
        )
        self.sio_connected = False
        self.command_buffer = []
        self.setup_socketio_events()

        if not self.use_server.get():
            self.after(100, self.connect_robot)
        else:
            self.start_socketio()

        self.buttons = {}
        self.button_images = {}
        self.dropdowns = {}
        self.tray_icon = None

        self.serial_thread = None
        self.serial_running = False
        self.serial_port = None

        self.grid_columnconfigure(tuple(range(9)), weight=1)
        self.create_ui()

        self.bind("<F3>", self.toggle_settings_panel)
        self.bind("<Unmap>", self.on_minimize)  # minimize to tray only
        
    def setup_socketio_events(self):
        @self.sio.event
        def connect():
            self.sio_connected = True
            self.set_status("WebSocket connected")
            if self.command_buffer:
                cmd = self.command_buffer.pop(0)
                try:
                    self.sio.emit('send_command', {'command': cmd})
                except Exception as e:
                    self.set_status(f"[WS ERROR] Failed to send buffered command: {e}")

        @self.sio.event
        def disconnect():
            self.sio_connected = False
            self.set_status("WebSocket disconnected")

        @self.sio.event
        def reconnect():
            self.set_status("WebSocket reconnecting...")

        @self.sio.on('command_response')
        def on_command_response(data):
            # Optional: process command responses here
            pass

        @self.sio.on('queued')
        def on_queued(data):
            # Optional: process queued confirmations here
            pass

    def start_socketio(self):
        def connect_loop():
            while True:
                try:
                    if not self.sio.connected:
                        self.sio.connect("http://localhost:5001")
                    while self.sio.connected:
                        time.sleep(1)
                except Exception as e:
                    self.set_status(f"SocketIO connect failed: {e}")
                    time.sleep(2)  # Short retry wait for local
        threading.Thread(target=connect_loop, daemon=True).start()

    def refresh_ports(self):
        ports = self.get_serial_ports()
        self.port_combo['values'] = ports
        if ports:
            self.port_var.set(ports[0])
        else:
            self.port_var.set("No ports")
        self.set_status("COM ports refreshed")

    def create_ui(self):
        start_col = 2
        display_labels = [label for label, _ in COMMAND_OPTIONS]

        for i, (label, color) in enumerate(BUTTONS):
            img = self.create_round_button_image(color, BUTTON_SIZE, BORDER_SIZE)
            img_hover = self.adjust_brightness(img, 0.85)
            photo = ImageTk.PhotoImage(img)
            photo_hover = ImageTk.PhotoImage(img_hover)

            btn = tk.Label(self, image=photo, bg="#efefef", cursor="hand2")
            btn.image_normal = photo
            btn.image_hover = photo_hover
            btn.image = photo
            btn.grid(row=0, column=start_col + i, pady=30)

            btn.bind("<Enter>", lambda e, b=btn: b.configure(image=b.image_hover))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(image=b.image_normal))
            btn.bind("<Button-1>", lambda e, l=label: self.on_button_press(l))

            self.buttons[label] = btn
            self.button_images[label] = (photo, photo_hover)

            # Preselect the corresponding label if available
            default_index = i + 1 if i + 1 < len(display_labels) else 0
            var = tk.StringVar(value=display_labels[default_index])
            dropdown = ttk.Combobox(self, values=display_labels, textvariable=var, state="readonly")
            dropdown.grid(row=1, column=start_col + i)
            self.dropdowns[label] = var

        self.status_var = tk.StringVar(value="Status: Ready")
        self.status_label = tk.Label(
            self,
            textvariable=self.status_var,
            bg="#efefef",
            font=("Segoe UI", 14),
            anchor="center"
        )
        self.status_label.grid(row=2, column=0, columnspan=9, pady=(20, 0))

        # Serial Settings groupbox
        self.settings_frame = tk.LabelFrame(self, text="Serial Settings", bg="#efefef")
        self.settings_frame.grid(row=3, column=0, columnspan=9, pady=(30, 0), padx=10, sticky="ew")
        self.settings_frame.grid_remove()

        self.port_var = tk.StringVar()
        self.baud_var = tk.StringVar(value="115200")

        port_label = tk.Label(self.settings_frame, text="Port:", bg="#efefef")
        port_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.port_combo = ttk.Combobox(self.settings_frame, textvariable=self.port_var, values=self.get_serial_ports(), state="readonly")
        self.port_combo.grid(row=0, column=1, padx=5, pady=5)

        baud_label = tk.Label(self.settings_frame, text="Baud:", bg="#efefef")
        baud_label.grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.baud_combo = ttk.Combobox(self.settings_frame, textvariable=self.baud_var, values=["9600", "115200", "57600"], state="readonly")
        self.baud_combo.grid(row=0, column=3, padx=5, pady=5)

        self.connect_button = tk.Button(self.settings_frame, text="Connect", command=self.connect_serial)
        self.connect_button.grid(row=0, column=4, padx=10, pady=5)

        refresh_btn = tk.Button(self.settings_frame, text="Refresh", command=self.refresh_ports)
        refresh_btn.grid(row=0, column=2, padx=5, pady=5, sticky="w")

        # Serial monitor box inside serial settings groupbox
        self.serial_log = ScrolledText(self.settings_frame, height=6, state="disabled", wrap="word")
        self.serial_log.grid(row=1, column=0, columnspan=5, padx=5, pady=10, sticky="ew")

        # New Server Settings groupbox below Serial Settings
        self.server_toggle_frame = tk.LabelFrame(self, text="Server Settings", bg="#efefef")
        self.server_toggle_frame.grid(row=4, column=0, columnspan=9, pady=(10, 0), padx=10, sticky="ew")

        tk.Checkbutton(
            self.server_toggle_frame,
            text="Use Flask Server",
            variable=self.use_server,
            command=self.on_toggle_mode,
            bg="#efefef",
            onvalue=True,
            offvalue=False
        ).pack(anchor="w", padx=10, pady=5)

        self.settings_frame.grid_remove()
        self.server_toggle_frame.grid_remove()

    def on_toggle_mode(self):
        if self.use_server.get():
            self.set_status("Switched to Flask server mode")
            if self.robot:
                try:
                    self.robot.Disconnect()
                except:
                    pass
                self.robot = None
            if not self.sio_connected:
                self.start_socketio()
        else:
            self.set_status("Switched to direct TCP mode")
            if self.sio_connected:
                self.sio.disconnect()
            self.connect_robot()

    def send_via_server(self, command):
        if not self.sio_connected or not self.sio.connected:
            # Buffer only the latest command; replace previous
            if self.command_buffer:
                self.command_buffer[0] = command
            else:
                self.command_buffer.append(command)
            self.set_status("WebSocket not connected, buffering command")
            return None, "Not connected"
        try:
            self.sio.emit('send_command', {'command': command})
            return "queued", None
        except Exception as e:
            self.set_status(f"[WS ERROR] {e}")
            return None, str(e)

    def connect_robot(self):
        try:
            self.robot = Dobot()
            self.robot.Connect()
            self.robot.EnableRobot()
            self.set_status("Robot connected and enabled")
            print("[ROBOT] Connected and enabled")
        except Exception as e:
            self.set_status(f"Robot connection failed: {e}")
            print(f"[ERROR] Robot connection failed: {e}")
            self.robot = None

    def log_serial_message(self, message):
        self.serial_log.configure(state="normal")
        self.serial_log.insert(tk.END, message + "\n")
        self.serial_log.see(tk.END)
        self.serial_log.configure(state="disabled")

    def create_round_button_image(self, color, size, border):
        img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.ellipse((0, 0, size - 1, size - 1), fill=color, outline="black", width=border)
        return img

    def adjust_brightness(self, img, factor):
        enhancer = ImageEnhance.Brightness(img)
        return enhancer.enhance(factor)

    def on_button_press(self, label):
        selected_label = self.dropdowns[label].get()
        match = next((cmd for lbl, cmd in COMMAND_OPTIONS if lbl == selected_label), None)
        if match is None:
            self.set_status(f"{label} → {selected_label} (no action)")
            return
        self.set_status(f"{label} → {selected_label}")
        self.flash_button(label)
        self.send_robot_command(match)

    def send_robot_command(self, command):
        print(command)
        if self.use_server.get():
            if isinstance(command, str):
                resp, err = self.send_via_server(f"{command}()")
                self.set_status(f"[SERVER] {command}: {resp or err}")
            elif isinstance(command, tuple):
                method, args = command
                argstr = ",".join(map(str, args))
                resp, err = self.send_via_server(f"{method}({argstr})")
                self.set_status(f"[SERVER] {method}: {resp or err}")
        else:
            if not self.robot:
                print("[ROBOT] Not connected")
                return
            try:
                if isinstance(command, str):
                    getattr(self.robot, command)()
                elif isinstance(command, tuple):
                    method, args = command
                    getattr(self.robot, method)(*args)
            except Exception as e:
                self.set_status(f"[ROBOT] {e}")

    def flash_button(self, label):
        btn = self.buttons.get(label)
        if not btn:
            return
        original = btn["image"]
        btn.configure(image=self.button_images[label][1])  # use hover (darker)
        self.after(200, lambda: btn.configure(image=self.button_images[label][0]))

    def toggle_settings_panel(self, event=None):
        self.expanded = not self.expanded
        if self.expanded:
            self.geometry(GUI_EXTENDED)
            self.settings_frame.grid()
            self.server_toggle_frame.grid()
        else:
            self.geometry(GUI_SIZE)
            self.settings_frame.grid_remove()
            self.server_toggle_frame.grid_remove()

    def get_serial_ports(self):
        ports = [p.device for p in serial.tools.list_ports.comports()]
        filtered = [p for p in ports if not p.upper().startswith("COM1")]
        self.port_var.set(filtered[0] if filtered else "No ports")
        return filtered if filtered else ["No ports"]

    def connect_serial(self):
        if self.serial_running:
            # Disconnect
            self.serial_running = False
            if self.serial_port and self.serial_port.is_open:
                self.serial_port.close()
            self.set_status("Disconnected")
            self.connect_button.config(text="Connect")
            return

        # Connect
        port = self.port_var.get()
        baud = int(self.baud_var.get())
        try:
            self.serial_port = serial.Serial(port, baud, timeout=1)
            self.set_status(f"Connected to {port} @ {baud} baud")
            self.connect_button.config(text="Disconnect")
            self.serial_running = True
            self.serial_thread = threading.Thread(target=self.read_serial, daemon=True)
            self.serial_thread.start()
        except Exception as e:
            self.set_status(f"Connection failed: {e}")
            print(f"[ERROR] Serial connection failed: {e}")

    def read_serial(self):
        while self.serial_running and self.serial_port and self.serial_port.is_open:
            try:
                raw = self.serial_port.readline()
                line = raw.decode("utf-8", errors="ignore").strip()
                if line:
                    self.after(0, lambda l=line: self.log_serial_message(l))
                    if line.startswith("BUTTON_"):
                        label = line.replace("BUTTON_", "").strip().upper()
                        self.after(0, lambda l=label: self.handle_serial_button(l))
            except Exception as e:
                print(f"[ERROR] Serial read failed: {e}")
                self.serial_running = False
                break

    def handle_serial_button(self, label):
        if label in self.dropdowns:
            self.on_button_press(label)
        else:
            print(f"[WARNING] Unknown button label from serial: {label}")

    def set_status(self, message):
        self.status_var.set(f"Status: {message}")

    def on_minimize(self, event):
        if self.state() == "iconic":
            self.after(200, self.minimize_to_tray)

    def minimize_to_tray(self):
        if self.tray_icon is not None:
            return  # already minimized

        self.withdraw()
        image = self.create_tray_icon_image()
        menu = pystray.Menu(
            pystray.MenuItem("Restore", self.restore_window),
            pystray.MenuItem("Exit", self.exit_app)
        )
        self.tray_icon = pystray.Icon("dobot_gui", image, "Dobot Control Panel", menu)

        def run_icon():
            self.tray_icon.run()
            self.tray_icon = None  # reset when closed

        threading.Thread(target=run_icon, daemon=True).start()

    def restore_window(self, icon=None, item=None):
        if self.tray_icon:
            self.tray_icon.stop()
            self.tray_icon = None
        self.deiconify()

    def exit_app(self, icon=None, item=None):
        self.serial_running = False
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
        if self.tray_icon:
            self.tray_icon.stop()
        self.destroy()
        sys.exit()

    def create_tray_icon_image(self):
        img = Image.new("RGB", (64, 64), "white")
        draw = ImageDraw.Draw(img)
        draw.ellipse((8, 8, 56, 56), fill="black")
        return img

if __name__ == "__main__":
    app = ControlPanel()
    app.mainloop()
