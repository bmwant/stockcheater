import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QScreen
from PyQt5.QtCore import QRect, QPoint, QSize

import config


def main():
    app = QApplication(sys.argv)
    screen = QScreen.grabWindow(
        app.primaryScreen(),
        QApplication.desktop().winId()
    )

    board_rect = QRect(
        QPoint(*config.BOARD_POINT),
        QSize(config.BOARD_SIZE, config.BOARD_SIZE)
    )
    size = config.CELL_SIZE
    board = screen.copy(board_rect)  # int x, int y, int width, int height
    for i in range(8):
        for j in range(8):
            r = QRect(i*size, j*size, size, size)
            c = board.copy(r)
            c.save(f'./pieces/{i}{j}.png')


if __name__ == '__main__':
    main()
