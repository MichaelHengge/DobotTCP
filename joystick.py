import pygame
import tkinter as tk

# Initialize pygame
pygame.init()
pygame.joystick.init()

# GUI setup
root = tk.Tk()
root.title("Joystick Test")
root.geometry("400x400")
canvas = tk.Canvas(root, width=400, height=500, bg="black", highlightthickness=0)
canvas.pack()

# Top buttons (1 and 2)
button_positions = [(120, 80), (280, 80)]
buttons = []
for x, y in button_positions:
    btn = canvas.create_oval(x - 30, y - 30, x + 30, y + 30, fill="gray")
    buttons.append(btn)

# Diagonal triangles for buttons 3 and 4
# Button 3: below Button 1, pointing up-left
# Button 4: below Button 2, pointing up-right
diagonals = {
    "B3": canvas.create_polygon(96.2, 141.3, 96.2, 177.4, 135.7, 141.3, fill="gray"),
    "B4": canvas.create_polygon(297.9, 141.3, 257.0, 141.3, 297.9, 177.4, fill="gray"),
}

# D-pad directional triangles
triangles = {
    "UP": canvas.create_polygon(200, 230, 180, 260, 220, 260, fill="gray"),
    "DOWN": canvas.create_polygon(200, 330, 180, 300, 220, 300, fill="gray"),
    "LEFT": canvas.create_polygon(130, 280, 160, 260, 160, 300, fill="gray"),
    "RIGHT": canvas.create_polygon(270, 280, 240, 260, 240, 300, fill="gray"),
}

# Update loop
def update():
    pygame.event.pump()
    if pygame.joystick.get_count() > 0:
        js = pygame.joystick.Joystick(0)
        x = js.get_axis(0)
        y = js.get_axis(1)

        # D-pad directions
        canvas.itemconfig(triangles["UP"], fill="red" if y < -0.5 else "gray")
        canvas.itemconfig(triangles["DOWN"], fill="red" if y > 0.5 else "gray")
        canvas.itemconfig(triangles["LEFT"], fill="red" if x < -0.5 else "gray")
        canvas.itemconfig(triangles["RIGHT"], fill="red" if x > 0.5 else "gray")

        # Buttons
        for i in range(min(4, js.get_numbuttons())):
            state = "red" if js.get_button(i) else "gray"
            if i < 2:
                canvas.itemconfig(buttons[i], fill=state)
            elif i == 2:
                canvas.itemconfig(diagonals["B3"], fill=state)
            elif i == 3:
                canvas.itemconfig(diagonals["B4"], fill=state)

    root.after(50, update)

update()
root.mainloop()
