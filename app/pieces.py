from app.position import Position


# Клас для опису кольору фігури
class Color(object):
    BLACK = -1
    EMPTY = 0
    WHITE = 1


# Клас для опису фігури
class Piece(object):
    image = None
    moves = []

    def __init__(self, color):
        self.color = color

    def __repr__(self):
        if self.color == Color.WHITE:
            return self.image[0]
        else:
            return self.image[1]

    def __eq__(self, another):
        return (type(self), self.color) == (type(another), another.color)

    # Метод, який повертає всі можливі клітинки для ходу даною фігурою
    def get_targets(self, position, board):
        result = []
        for single_direction_moves in self.moves:
            for single_direction_move in single_direction_moves:
                x_target = position.x + single_direction_move[0]
                y_target = position.y + single_direction_move[1]
                if 0 <= x_target <= 7 and 0 <= y_target <= 7:
                    target_piece = board[x_target][y_target]
                    if target_piece.color != self.color:
                        result.append(Position(x_target, y_target))
                    if target_piece.color != Color.EMPTY:
                        break
        return result


class Empty(object):
    color = Color.EMPTY

    def get_targets(self):
        raise Exception('Empty square does not have moves!')  # Помилка при намаганні взяти можливі клітинки для ходу у порожньої клітинки

    def __repr__(self):
        return ''


# Клас пішка
class Pawn(Piece):
    image = ('♙', '♟')

    def get_targets(self, position, board):
        result = []
        if self.color == Color.WHITE:
            x_target = position.x - 1
            y_target = position.y + 1
            if 0 <= x_target <= 7 and 0 <= y_target <= 7 and board[x_target][y_target].color == Color.BLACK:
                result.append(Position(x_target, y_target))
            x_target = position.x + 1
            y_target = position.y + 1
            if 0 <= x_target <= 7 and 0 <= y_target <= 7 and board[x_target][y_target].color == Color.BLACK:
                result.append(Position(x_target, y_target))
            x_target = position.x
            y_target = position.y + 1
            if 0 <= x_target <= 7 and 0 <= y_target <= 7 and board[x_target][y_target].color == Color.EMPTY:
                result.append(Position(x_target, y_target))
            if position.y == 1:
                x_target = position.x
                y_target = position.y + 2
                if 0 <= x_target <= 7 and 0 <= y_target <= 7 and board[x_target][y_target - 1].color == board[x_target][y_target].color == Color.EMPTY:
                    result.append(Position(x_target, y_target))
        else:
            x_target = position.x - 1
            y_target = position.y - 1
            if 0 <= x_target <= 7 and 0 <= y_target <= 7 and board[x_target][y_target].color == Color.WHITE:
                result.append(Position(x_target, y_target))
            x_target = position.x + 1
            y_target = position.y - 1
            if 0 <= x_target <= 7 and 0 <= y_target <= 7 and board[x_target][y_target].color == Color.WHITE:
                result.append(Position(x_target, y_target))
            x_target = position.x
            y_target = position.y - 1
            if 0 <= x_target <= 7 and 0 <= y_target <= 7 and board[x_target][y_target].color == Color.EMPTY:
                result.append(Position(x_target, y_target))
            if position.y == 6:
                x_target = position.x
                y_target = position.y - 2
                if 0 <= x_target <= 7 and 0 <= y_target <= 7 and board[x_target][y_target + 1].color == board[x_target][y_target].color == Color.EMPTY:
                    result.append(Position(x_target, y_target))
        return result


# Клас тура
class Rook(Piece):
    image = ('♖', '♜')
    moves = [
        [
            [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0]  # right
        ],
        [
            [-1, 0], [-2, 0], [-3, 0], [-4, 0], [-5, 0], [-6, 0], [-7, 0]  # left
        ],
        [
            [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7]  # up
        ],
        [
            [0, -1], [0, -2], [0, -3], [0, -4], [0, -5], [0, -6], [0, -7]  # down
        ]
    ]


# Клас кінь
class Knight(Piece):
    image = ('♘', '♞')
    moves = [[[1, 2]], [[2, 1]], [[2, -1]], [[1, -2]], [[-1, -2]], [[-2, -1]], [[-2, 1]], [[-1, 2]]]


# Клас ферзь
class Bishop(Piece):
    image = ('♗', '♝')
    moves = [
        [
            [1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7]  # right-up
        ],
        [
            [1, -1], [2, -2], [3, -3], [4, -4], [5, -5], [6, -6], [7, -7]  # right-down
        ],
        [
            [-1, 1], [-2, 2], [-3, 3], [-4, 4], [-5, 5], [-6, 6], [-7, 7]  # left-up
        ],
        [
            [-1, -1], [-2, -2], [-3, -3], [-4, -4], [-5, -5], [-6, -6], [-7, -7]  # left-down
        ]
    ]


# Клас королева
class Queen(Piece):
    image = ('♕', '♛')
    moves = [
        [
            [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0]  # right
        ],
        [
            [-1, 0], [-2, 0], [-3, 0], [-4, 0], [-5, 0], [-6, 0], [-7, 0]  # left
        ],
        [
            [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7]  # up
        ],
        [
            [0, -1], [0, -2], [0, -3], [0, -4], [0, -5], [0, -6], [0, -7]  # down
        ],
        [
            [1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7]  # right-up
        ],
        [
            [1, -1], [2, -2], [3, -3], [4, -4], [5, -5], [6, -6], [7, -7]  # right-down
        ],
        [
            [-1, 1], [-2, 2], [-3, 3], [-4, 4], [-5, 5], [-6, 6], [-7, 7]  # left-up
        ],
        [
            [-1, -1], [-2, -2], [-3, -3], [-4, -4], [-5, -5], [-6, -6], [-7, -7]  # left-down
        ]
    ]


# Клас король
class King(Piece):
    image = ('♔', '♚')
    moves = [[[0, 1]], [[1, 1]], [[1, 0]], [[1, -1]], [[0, -1]], [[-1, -1]], [[-1, 0]], [[-1, 1]]]
