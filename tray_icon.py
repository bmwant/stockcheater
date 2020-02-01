from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


def tray_icon():
    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)

    # Create the icon
    icon = QIcon("icon.png")

    # Create the tray
    tray = QSystemTrayIcon()
    tray.setIcon(icon)
    tray.setVisible(True)

    # Create the menu
    menu = QMenu()
    action = QAction("A menu item")
    menu.addAction(action)

    # Add the menu to the tray
    tray.setContextMenu(menu)

    app.exec_()


SIZE = 73


def screenshot():
    import sys
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtGui import QPixmap, QScreen
    from datetime import datetime
    from PyQt5.QtCore import QRect

    date = datetime.now()
    filename = date.strftime('%Y-%m-%d_%H-%M-%S.jpg')
    app = QApplication(sys.argv)
    screen = QScreen.grabWindow(app.primaryScreen(), QApplication.desktop().winId())

    board_rect = QRect(10, 20, 584, 584)
    board = screen.copy(board_rect)  # int x, int y, int width, int height
    for i in range(8):
        for j in range(8):
            r = QRect(i*SIZE, j*SIZE, SIZE, SIZE)
            c = board.copy(r)
            c.save(f'cells/c{i}{j}.png')


if __name__ == '__main__':
    screenshot()
