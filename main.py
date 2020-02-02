import sys

from PyQt5 import QtGui, QtCore, uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication,
    QMenu,
    QSystemTrayIcon,
    QAction,
)
from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtGui import QScreen, QPainter, QPen, QIcon

import grab_pieces


SIZE = 73
BOARD_SIZE = 584


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.X11BypassWindowManagerHint
        )
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # x, y, width, height
        self.setGeometry(700, 400, BOARD_SIZE, BOARD_SIZE)
        # self.setGeometry(
        #     QtWidgets.QStyle.alignedRect(
        #         QtCore.Qt.LeftToRight, QtCore.Qt.AlignCenter,
        #         QtCore.QSize(600, 600),
        #         QtWidgets.qApp.desktop().availableGeometry()
        # ))
        self.setWindowOpacity(0.8)

    def mousePressEvent(self, event):
        self.hide()
        # QtWidgets.qApp.quit()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))

        painter.drawLine(20, 20, 100, 140)

    def activate(self):
        self.show()

    def shot(self):
        grab_pieces.main()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    mywindow = MainWindow()

    icon = QIcon("icon.png")
    # Create the tray
    tray = QSystemTrayIcon()
    tray.setIcon(icon)
    tray.setVisible(True)

    # Create the menu
    menu = QMenu()
    show_action = QAction('Show move')
    shot_action = QAction('Shot')
    exit_action = QAction('Exit')
    menu.addAction(show_action)
    menu.addAction(shot_action)
    menu.addAction(exit_action)
    show_action.triggered.connect(mywindow.activate)
    shot_action.triggered.connect(mywindow.shot)
    exit_action.triggered.connect(QtWidgets.qApp.quit)

    # Add the menu to the tray
    tray.setContextMenu(menu)
    mywindow.show()
    app.exec_()
