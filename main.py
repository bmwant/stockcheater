import sys

import chess
from chess import engine as chess_engine
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
from PyQt5.QtGui import QPainter, QPen, QIcon

import fen
import config
import recognizer
import grab_pieces


class MainWindow(QMainWindow):

    _engine = None

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
        self.setGeometry(*config.BOARD_POINT,
                         config.BOARD_SIZE, config.BOARD_SIZE)
        self.setWindowOpacity(0.8)

        self.is_white = True
        self.white_checkbox = QAction('White', checkable=True, checked=True)
        self.white_checkbox.triggered.connect(self.set_white)
        self.black_checkbox = QAction('Black', checkable=True)
        self.black_checkbox.triggered.connect(self.set_black)

        self.recognizer = recognizer.Recognizer()

        self.point_from = None
        self.point_to = None

        # init engine
        self.engine  # noqa

    def __del__(self):
        if self._engine is not None:
            self._engine.quit()

    @property
    def engine(self):
        if self._engine is None:
            self._engine = chess_engine.SimpleEngine.popen_uci(config.ENGINE_PATH)
        return self._engine

    def mousePressEvent(self, event):
        self.hide()
        # QtWidgets.qApp.quit()

    def paintEvent(self, event):
        if self.point_from is None or self.point_to is None:
            return
        painter = QPainter(self)
        painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))

        painter.drawLine(self.point_from, self.point_to)

        painter.setPen(QPen(Qt.blue, 2, Qt.SolidLine))
        painter.drawRect(0, 0, config.BOARD_SIZE, config.BOARD_SIZE)

    def show_move(self):
        self.suggest_move()
        self.show()

    def suggest_move(self):
        filename = grab_pieces.shot_board(QtWidgets.qApp)
        board_arr = self.recognizer.recognize_board(filename)
        board_fen = fen.create_fen(board_arr, white=self.is_white)
        board = chess.Board(fen=board_fen)
        result = self.engine.play(board, chess_engine.Limit(time=0.1))
        line = fen.uci_move_to_line(result.move.uci())
        self.point_from = QPoint(*line.from_)
        self.point_to = QPoint(*line.to_)
        self.update()

    def set_white(self):
        self.is_white = True
        self.white_checkbox.setChecked(True)
        self.black_checkbox.setChecked(False)

    def set_black(self):
        self.is_white = False
        self.white_checkbox.setChecked(False)
        self.black_checkbox.setChecked(True)


def init_application():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    mywindow = MainWindow()

    icon = QIcon('icon.png')
    # Create the tray
    tray = QSystemTrayIcon()
    tray.setIcon(icon)
    tray.setVisible(True)

    # Create the menu
    menu = QMenu()
    color_menu = QMenu('Player color')
    color_menu.addAction(mywindow.white_checkbox)
    color_menu.addAction(mywindow.black_checkbox)

    show_action = QAction('Show move')
    nothing_action = QAction('Nothing')
    exit_action = QAction('Exit')
    menu.addAction(show_action)
    menu.addMenu(color_menu)
    menu.addAction(nothing_action)
    menu.addAction(exit_action)
    show_action.triggered.connect(mywindow.show_move)
    exit_action.triggered.connect(QtWidgets.qApp.quit)

    # Add the menu to the tray
    tray.setContextMenu(menu)
    mywindow.show()
    app.exec_()


if __name__ == '__main__':
    # for debugging
    # from PyQt5.QtCore import pyqtRemoveInputHook
    init_application()
