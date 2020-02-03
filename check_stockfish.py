import chess

from chess import svg
from chess import engine


FEN = 'rnbqkbnr/pppppp1p/6p1/8/3P4/5N2/PPP1PPPP/RNBQKB1R w KQkq - 0 1'

board = chess.Board(fen=FEN)


def save_pic(board):
    pic = svg.board(board=board)
    with open('pic.svg', 'w') as f:
        f.write(pic)


def check_engine():
    eng = engine.SimpleEngine.popen_uci("./src/stockfish")
    result = eng.play(board, chess.engine.Limit(time=0.1))
    board.push(result.move)
    save_pic(board)
    eng.quit()


def make_screenshot():
    import pyscreenshot

    im = pyscreenshot.grab()
    im.save('ss.png')


if __name__ == '__main__':
    make_screenshot()
