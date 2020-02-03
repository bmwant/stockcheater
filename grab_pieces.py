import os
import sys
import tempfile

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QScreen
from PyQt5.QtCore import QRect, QPoint, QSize

import config


def screenshot(app):
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
            r = QRect(i * size, j * size, size, size)
            c = board.copy(r)
            c.save(f'./pieces/{i}{j}.png')


def shot_board(app) -> str:
    screen = QScreen.grabWindow(
        app.primaryScreen(),
        QApplication.desktop().winId()
    )

    board_rect = QRect(
        QPoint(*config.BOARD_POINT),
        QSize(config.BOARD_SIZE, config.BOARD_SIZE)
    )
    board = screen.copy(board_rect)
    filename = '{}.png'.format(next(tempfile._get_candidate_names()))
    filepath = os.path.join(tempfile._get_default_tempdir(), filename)
    board.save(filepath)
    return filepath


def main():
    app = QApplication(sys.argv)
    screenshot(app)


if __name__ == '__main__':
    main()
