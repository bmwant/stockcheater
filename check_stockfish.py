import chess

from chess import svg
from chess import engine


# FEN = 'rnbqkbnr/pp2pppp/2p5/3P4/8/5N2/PPPP1PPP/RNBQKB1R b KQkq - 0 1'
FEN = 'r4rk1/1pq1bpp1/2n1pn1p/1NPp4/3P4/P2Q1N2/5PPP/R1B1R1K1 b KQkq - 0 1'

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
    # make_screenshot()
    save_pic(board)
