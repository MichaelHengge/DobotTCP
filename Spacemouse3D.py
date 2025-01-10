import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import pyspacemouse  # Import the pyspacemouse library

# Define the vertices and edges of the cube
vertices = [
    [1, 1, -1],
    [1, -1, -1],
    [-1, -1, -1],
    [-1, 1, -1],
    [1, 1, 1],
    [1, -1, 1],
    [-1, -1, 1],
    [-1, 1, 1],
]

edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]

def draw_cube():
    glColor3f(1, 1, 1)  # Set cube color to white
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def draw_gui_axes():
    """Draw small axis arrows in the lower-right corner of the GUI window."""
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, 800, 600, 0, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glLineWidth(2)
    glBegin(GL_LINES)

    # X-axis (Left/Right, Blue)
    glColor3f(0, 0, 1)
    glVertex2f(750, 550)
    glVertex2f(780, 550)

    # Z-axis (Up/Down, Red)
    glColor3f(1, 0, 0)
    glVertex2f(750, 550)
    glVertex2f(750, 520)

    # Y-axis (In/Out, Green)
    glColor3f(0, 1, 0)
    glVertex2f(750, 550)
    glVertex2f(770, 530)

    glEnd()

    # Draw arrowheads
    glBegin(GL_TRIANGLES)

    # X-axis arrowhead (Blue)
    glColor3f(0, 0, 1)
    glVertex2f(780, 550)
    glVertex2f(775, 555)
    glVertex2f(775, 545)

    # Z-axis arrowhead (Red)
    glColor3f(1, 0, 0)
    glVertex2f(750, 520)
    glVertex2f(745, 525)
    glVertex2f(755, 525)

    # Y-axis arrowhead (Green)
    glColor3f(0, 1, 0)
    glVertex2f(770, 530)
    glVertex2f(765, 535)
    glVertex2f(765, 525)

    glEnd()

    # Draw axis labels
    draw_text("X", 785, 540, font_size=18, color=(0, 0, 255))  # Blue
    draw_text("Y", 765, 515, font_size=18, color=(0, 255, 0))  # Green
    draw_text("Z", 735, 515, font_size=18, color=(255, 0, 0))  # Red

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_text(text, x, y, font_size=18, color=(255, 255, 255)):
    """Render text using Pygame and display it using OpenGL."""
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color, (0, 0, 0, 0))  # Transparent background
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    width, height = text_surface.get_size()

    # Set up OpenGL for 2D rendering
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, 800, 600, 0, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)

    # Render the text as a bitmap
    glDrawPixels(width, height, GL_RGBA, GL_UNSIGNED_BYTE, text_data)

    # Restore OpenGL state
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_button_states(button_states):
    """Draw the SpaceMouse button states."""
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, 800, 600, 0, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    # Button 1 graphical representation
    glBegin(GL_QUADS)
    glColor3f(0, 1, 0) if button_states[0] else glColor3f(1, 0, 0)  # Green if pressed, red otherwise
    glVertex2f(10, 160)
    glVertex2f(50, 160)
    glVertex2f(50, 200)
    glVertex2f(10, 200)
    glEnd()

    # Button 2 graphical representation
    glBegin(GL_QUADS)
    glColor3f(0, 1, 0) if button_states[1] else glColor3f(1, 0, 0)  # Green if pressed, red otherwise
    glVertex2f(60, 160)
    glVertex2f(100, 160)
    glVertex2f(100, 200)
    glVertex2f(60, 200)
    glEnd()

    # Button 1 label
    draw_text("Button 1", 15, 205, font_size=18, color=(255, 255, 255))

    # Button 2 label
    draw_text("Button 2", 65, 205, font_size=18, color=(255, 255, 255))

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("3D Cube with Text")

    # Initialize the SpaceMouse
    pyspacemouse.open()

    # Set up the perspective
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    # Initial rotation values
    rotation_roll = 0
    rotation_pitch = 0
    rotation_yaw = 0

    # Initial translation values
    translation_x = 0
    translation_y = 0
    translation_z = -5

    # Apply initial rotation for corner view
    initial_roll = -25  # Adjust sign for correct direction
    initial_pitch = -25  # Adjust sign for correct direction
    initial_yaw = 45  # Adjust sign for correct direction

    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pyspacemouse.close()  # Close SpaceMouse connection
                pygame.quit()
                quit()

        # Read the SpaceMouse state
        state = pyspacemouse.read()
        x = state.x if abs(state.x) > 0.05 else 0  # Deadzone for X
        y = state.y if abs(state.y) > 0.05 else 0  # Deadzone for Y
        z = state.z if abs(state.z) > 0.05 else 0  # Deadzone for Z
        roll = state.roll if abs(state.roll) > 0.05 else 0  # Deadzone for Roll
        pitch = state.pitch if abs(state.pitch) > 0.05 else 0  # Deadzone for Pitch
        yaw = state.yaw if abs(state.yaw) > 0.05 else 0  # Deadzone for Yaw
        buttons = state.buttons

        # Update rotation values with scaled speed based on input magnitude
        rotation_roll += -roll * abs(roll) * 10  # Scale with magnitude, adjust sign for direction
        rotation_pitch += -pitch * abs(pitch) * 10
        rotation_yaw += yaw * abs(yaw) * 10  # Fixed inversion for yaw

        # Update translation values with scaled speed based on input magnitude
        translation_x += x * abs(x) * 0.1
        translation_y += y * abs(y) * 0.1
        translation_z += z * abs(z) * 0.1

        # Clear OpenGL buffers
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Apply translations and rotations
        glPushMatrix()
        glTranslatef(translation_x, translation_y, translation_z)  # Apply translation
        glRotatef(initial_roll + rotation_roll, 0, 0, 1)  # Roll
        glRotatef(initial_pitch + rotation_pitch, 1, 0, 0)  # Pitch
        glRotatef(initial_yaw + rotation_yaw, 0, 1, 0)  # Yaw

        draw_cube()
        glPopMatrix()

        # Draw small axes in the GUI
        draw_gui_axes()

        # Render SpaceMouse data as text
        draw_text(f"X: {x:.2f}", 10, 20, font_size=18, color=(255, 255, 255))
        draw_text(f"Y: {y:.2f}", 10, 35, font_size=18, color=(255, 255, 255))
        draw_text(f"Z: {z:.2f}", 10, 50, font_size=18, color=(255, 255, 255))
        draw_text(f"Roll: {roll:.2f}", 10, 65, font_size=18, color=(255, 255, 255))
        draw_text(f"Pitch: {pitch:.2f}", 10, 80, font_size=18, color=(255, 255, 255))
        draw_text(f"Yaw: {yaw:.2f}", 10, 95, font_size=18, color=(255, 255, 255))

        # Display button states
        draw_button_states(buttons)

        pygame.display.flip()
        clock.tick(400)

if __name__ == "__main__":
    main()
