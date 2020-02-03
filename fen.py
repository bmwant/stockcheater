from dataclasses import dataclass

import config


def create_fen(board_arr: list, white: bool) -> str:
    color = 'w' if white else 'b'
    if not white:
        reversed_board = []
        for row in reversed(board_arr):
            reversed_board.append(reversed(row))
        board_arr = reversed_board

    board = ''
    # top to bottom, left to right as of white's perspective
    for row in board_arr:
        ec = 0  # empty cells counter
        line = ''
        for p in row:
            if p != '-':
                if ec:
                    line += str(ec)
                    ec = 0
                line += p
            else:
                ec += 1
        if ec:
            line += str(ec)  # end of row might be empty
        board += f'{line}/'
    board = board[:-1]  # remove trailing slash
    fen = f'{board} {color} KQkq - 0 1'
    return fen


@dataclass
class Line:
    from_: tuple
    to_: tuple


def uci_move_to_line(move, white: bool=True) -> Line:
    from_cell = move[:2]
    to_cell = move[-2:]

    offset = config.CELL_SIZE / 2
    x1 = (ord(from_cell[0]) - ord('a')) * config.CELL_SIZE + offset
    y1 = config.BOARD_SIZE - (int(from_cell[1]) - 1) * config.CELL_SIZE - offset

    x2 = (ord(to_cell[0]) - ord('a')) * config.CELL_SIZE + offset
    y2 = config.BOARD_SIZE - (int(to_cell[1]) - 1) * config.CELL_SIZE - offset

    if white:
        x1 = config.BOARD_SIZE - x1
        y1 = config.BOARD_SIZE - y1
        x2 = config.BOARD_SIZE - x2
        y2 = config.BOARD_SIZE - y2

    # print('x1, y1', x1, y1)
    # print('x2, y2', x2, y2)

    line = Line(from_=(x1, y1), to_=(x2, y2))
    return line

