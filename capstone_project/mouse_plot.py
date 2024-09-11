import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QOpenGLWidget
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtCore import Qt
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import gluPerspective, gluLookAt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("3D Point Manipulation")
        self.setGeometry(100, 100, 800, 600)

        self.gl_widget = OpenGLWidget(self)
        self.setCentralWidget(self.gl_widget)


class OpenGLWidget(QOpenGLWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.x_pos = 0
        self.y_pos = 0
        self.z_pos = 0  # Initial z position

    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)
        glClearColor(1.0, 1.0, 1.0, 1.0)  # Set white background color

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = w / h
        gluPerspective(45, aspect, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(5, 5, 5, 0, 0, 0, 0, 1, 0)  # Set camera position and orientation

        # Draw grids
        glColor3f(0.5, 0.5, 0.5)  # Grid color
        glBegin(GL_LINES)
        for i in range(-10, 11):  # Grid lines in x direction
            glVertex3f(i, -10, 0)
            glVertex3f(i, 10, 0)
        for i in range(-10, 11):  # Grid lines in y direction
            glVertex3f(-10, i, 0)
            glVertex3f(10, i, 0)
        for i in range(-10, 11):  # Grid lines in z direction
            glVertex3f(0, -10, i)
            glVertex3f(0, 10, i)
        glEnd()

        # Draw a point at the current position
        glPointSize(10)
        glBegin(GL_POINTS)
        glColor3f(1.0, 0.0, 0.0)
        glVertex3f(self.x_pos, self.y_pos, self.z_pos)
        glEnd()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.LeftButton:
            x = event.x()
            y = event.y()
            self.x_pos = (2 * x - self.width()) / self.width()
            self.y_pos = -(2 * y - self.height()) / self.height()
            self.update()

    def wheelEvent(self, event):
        delta = event.angleDelta().y() / 120
        self.z_pos += delta * 0.1  # Adjust the speed of movement
        self.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
