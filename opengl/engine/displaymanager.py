from OpenGL.GL import glViewport
from OpenGL.GLUT import (glutCreateWindow, glutDestroyWindow, glutHideWindow,
                         glutInit, glutInitWindowSize)

WIDTH = 800
HEIGHT = 600


class DisplayManager:

    @staticmethod
    def create_display(width=WIDTH, height=HEIGHT) -> int:
        glutInit([])
        glutInitWindowSize(width, height)
        window_id = glutCreateWindow('Test window title')
        glutHideWindow()

        glViewport(0, 0, width, height)

        return window_id

    @staticmethod
    def close_display(window_id: int):
        glutDestroyWindow(window_id)
