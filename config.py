CLASS_NAMES = (
    'r',  # black rook
    'n',  # black night
    'b',  # black bishop
    'q',  # black queen
    'k',  # black king
    'p',  # black pawn
    'R',  # white rook
    'N',  # white night
    'B',  # white bishop
    'Q',  # white queen
    'K',  # white king
    'P',  # white pawn
    '-',  # empty cell
)
MODEL_CHECKPOINT = './checkpoints/model_weights.ckpt'
INPUT_SHAPE = (26, 26)
DATASET_PATH = 'dataset.np'

# TOP-LEFT corner of the board relative to the screen (x, y) pair
BOARD_POINT = (634, 194)
# Size of a board in pixels as displayed on a screen
BOARD_SIZE = 632
# Size of a single board cell in pixel as displayed on a screen
# Usually it is just 1/8 of board size if no offset is present
CELL_SIZE = BOARD_SIZE / 8
