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
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def draw_text(text, x, y, font_size=24, color=(255, 255, 255)):
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
        x = state.x
        y = state.y
        z = state.z
        roll = state.roll
        pitch = state.pitch
        yaw = state.yaw

        # Update rotation values with scaled speed based on input magnitude
        rotation_roll += -roll * abs(roll) * 10  # Scale with magnitude, adjust sign for direction
        rotation_pitch += -pitch * abs(pitch) * 10
        rotation_yaw += -yaw * abs(yaw) * 10

        # Clear OpenGL buffers
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Apply rotations
        glPushMatrix()
        glRotatef(initial_roll + rotation_roll, 0, 0, 1)  # Roll
        glRotatef(initial_pitch + rotation_pitch, 1, 0, 0)  # Pitch
        glRotatef(initial_yaw + rotation_yaw, 0, 1, 0)  # Yaw

        draw_cube()
        glPopMatrix()

        # Render SpaceMouse data as text
        draw_text(f"X: {x:.2f}", 10, 20, font_size=18, color=(255, 255, 255))
        draw_text(f"Y: {y:.2f}", 10, 35, font_size=18, color=(255, 255, 255))
        draw_text(f"Z: {z:.2f}", 10, 50, font_size=18, color=(255, 255, 255))
        draw_text(f"Roll: {roll:.2f}", 10, 65, font_size=18, color=(255, 255, 255))
        draw_text(f"Pitch: {pitch:.2f}", 10, 80, font_size=18, color=(255, 255, 255))
        draw_text(f"Yaw: {yaw:.2f}", 10, 95, font_size=18, color=(255, 255, 255))

        pygame.display.flip()
        clock.tick(240)

if __name__ == "__main__":
    main()
