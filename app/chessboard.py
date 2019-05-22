import string

from app.pieces import Color, Empty, Pawn, Rook, Knight, Bishop, Queen, King
from app.position import Position
from app.repository import Repository

POSITIONS_DELIMITER = ':'  # Символ для розмежування позицій в рамках ходу збереженої гри
MOVEMENTS_DELIMITER = '#'  # Символ для розмежування ходів в рамках збереженої гри

repository = Repository()  # Об'єкт типу Repository для виклику методів класу Repository для роботи з базою даних


class Chessboard(object):  # Клас Chessboard який наслідує object

    def __init__(self):  # Метод ініціалізації початкових значень для об'єкта класа Chessboard
        self.movements_history = []  # Історія ходів для подальшого збереження гри
        self.current_player_color = Color.WHITE  # Колір поточного гравця
        self.captured_white_pieces = []  # Фігури, побиті чорними
        self.captured_black_pieces = []  # Фігури, побиті білими
        self.board = [  # Встановлення фігур на початкові позиції
            [Rook(Color.WHITE), Pawn(Color.WHITE), Empty(), Empty(), Empty(), Empty(), Pawn(Color.BLACK), Rook(Color.BLACK)],
            [Knight(Color.WHITE), Pawn(Color.WHITE), Empty(), Empty(), Empty(), Empty(), Pawn(Color.BLACK), Knight(Color.BLACK)],
            [Bishop(Color.WHITE), Pawn(Color.WHITE), Empty(), Empty(), Empty(), Empty(), Pawn(Color.BLACK), Bishop(Color.BLACK)],
            [Queen(Color.WHITE), Pawn(Color.WHITE), Empty(), Empty(), Empty(), Empty(), Pawn(Color.BLACK), Queen(Color.BLACK)],
            [King(Color.WHITE), Pawn(Color.WHITE), Empty(), Empty(), Empty(), Empty(), Pawn(Color.BLACK), King(Color.BLACK)],
            [Bishop(Color.WHITE), Pawn(Color.WHITE), Empty(), Empty(), Empty(), Empty(), Pawn(Color.BLACK), Bishop(Color.BLACK)],
            [Knight(Color.WHITE), Pawn(Color.WHITE), Empty(), Empty(), Empty(), Empty(), Pawn(Color.BLACK), Knight(Color.BLACK)],
            [Rook(Color.WHITE), Pawn(Color.WHITE), Empty(), Empty(), Empty(), Empty(), Pawn(Color.BLACK), Rook(Color.BLACK)]
        ]

    # Метод для перевірки, чи може поточний гравець походити даною фігурою
    def is_piece_allowed(self, position):
        current_position = self.parse_position(position)
        piece = self.board[current_position.x][current_position.y]
        return piece.color == self.current_player_color  # Повернути результат умови, що кольори фігури та поточного гравця рівні

    # Метод для вираховування можливих клітинок для ходів для позиції в стилі a1-h8
    def get_targets_of_unparsed_position(self, position):
        current_position = self.parse_position(position)
        return self.get_targets_of_parsed_position(current_position)

    # Метод для вираховування можливих клітинок для ходів для позиції в стилі 00-77
    def get_targets_of_parsed_position(self, position: Position):
        piece = self.board[position.x][position.y]  # Взяти фігуру на позиції [x, y]
        targets = piece.get_targets(position, self.board)  # Вирахувати можливі клітинки для ходу для заданої позиції

        result = []
        for target in targets:
            if not self.is_self_check_possible(position, target):  # Якщо потенційний хід не відкриє короля для шаху
                result.append(string.ascii_lowercase[target.x] + str(target.y + 1))  # Додати клітинку в список можливих клітинок для ходу
        return result

    # Метод для виконання ходу з позиції 'position' на позицію 'target'
    def perform_movement(self, position, target):
        current_position = self.parse_position(position)  # Позиція, звідки робиться хід
        target_position = self.parse_position(target)  # Позиція, куди робиться хід

        target_piece = self.board[target_position.x][target_position.y]  # Фігура, на яку робиться хід (може бути порожня клітинка)
        if target_piece.color == Color.WHITE:  # Якщо позиція куди робиться хід - біла фігура, то поповнити список збитих білих фігур
            self.captured_white_pieces.append(target_piece)
        else:  # Якщо позиція куди робиться хід - чорна фігура, то поповнити список збитих чорних фігур
            self.captured_black_pieces.append(target_piece)
        self.board[target_position.x][target_position.y] = self.board[current_position.x][current_position.y]  # Переставити фігуру на нову позицію
        self.board[current_position.x][current_position.y] = Empty()  # Очистити стару позицію
        self.current_player_color *= (-1)  # Змінити поточного гравця
        self.movements_history.append(self.construct_movement_string(current_position, target_position))  # Додати хід в історію ходів

        return self.is_check_for_current_player()  # Повернути значення, чи є шах після виконання ходу

    # Метод для переведення позиції з формату a1-h8 в формат 00-77
    def parse_position(self, position):
        x_position = string.ascii_lowercase.index(position[0])  # Позиція x - зліва направо
        y_position = int(position[1]) - 1  # Позиція y - знизу вгору
        return Position(x_position, y_position)

    # Повернути позицію короля для поточного гравця
    def get_king_position(self, color):
        for x_index, line in enumerate(self.board):  # Пошук короля поточного кольору на всій шаховій дошці
            for y_index, square in enumerate(line):
                if square == King(color):
                    return Position(x_index, y_index)

    # Перевірка, чи станеться шах для свого короля після виконання ходу
    def is_self_check_possible(self, position, target):
        target_piece = self.board[target.x][target.y]  # Виконати потенційний хід
        self.board[target.x][target.y] = self.board[position.x][position.y]
        self.board[position.x][position.y] = Empty()

        result = self.is_check_for_current_player()  # Перевірка, чи є шах для поточного гравця

        self.board[position.x][position.y] = self.board[target.x][target.y]  # Повернути хід назад
        self.board[target.x][target.y] = target_piece

        return result

    # Перевірка, чи є шах для поточного гравця
    def is_check_for_current_player(self):
        king_position = self.get_king_position(self.current_player_color)  # Взяти позицію короля

        for x_index, line in enumerate(self.board):  # Для всіх фігур суперника перевірити, чи є хоч одна, для якої можливий хід - це король поточного гравця
            for y_index, square in enumerate(line):
                if square.color == self.current_player_color * (-1):
                    for target in square.get_targets(Position(x_index, y_index), self.board):
                        if king_position == target:
                            return True
        return False

    # Перевірити, чи є мат для поточного гравця
    def is_checkmate_for_current_player(self):
        if not self.is_check_for_current_player():  # Перевірити, чи є шах
            return False
        else:
            for x_index, line in enumerate(self.board):  # Для всіх фігур поточного гравця перевірити, чи зникне шах після будь якого можливого ходу
                for y_index, square in enumerate(line):
                    if square.color == self.current_player_color:
                        targets = self.get_targets_of_parsed_position(Position(x_index, y_index))
                        if len(targets) > 0:
                            return False
        return True

    # Метод дя збереження гри
    def save_game(self, game_name):
        repository.save_game(game_name, MOVEMENTS_DELIMITER.join(self.movements_history))

    # Метод для створення рядка, який являє собою всі ходи гри, яку збираються зберегти
    def construct_movement_string(self, current_position, target_position):
        parsed_current_position = string.ascii_lowercase[current_position.x] + str(current_position.y + 1)
        parsed_target_position = string.ascii_lowercase[target_position.x] + str(target_position.y + 1)
        return POSITIONS_DELIMITER.join([parsed_current_position, parsed_target_position])

    # Метод для вибирання з бази даних всіх збережених ігор
    def get_games(self):
        return repository.get_games()

    # Метод для вибирання з бази даних інформації про ходи збереженої гри за її назвою
    def get_game_activity(self, game_name):
        result = []
        game_activity = repository.get_game(game_name)[0]  # Вибрати з бази даних інформацію про ходи збереженої гри
        movements = game_activity.split(MOVEMENTS_DELIMITER)  # Створити список ходів
        for movement in movements:
            result.append(movement.split(POSITIONS_DELIMITER))
        return result

    # Метод для розміщення всіх фігур на дошці на свої початкові позиції
    def clear_board(self):
        self.movements_history = []
        self.current_player_color = Color.WHITE
        self.captured_white_pieces = []
        self.captured_black_pieces = []
        self.board = [
            [Rook(Color.WHITE), Pawn(Color.WHITE), Empty(), Empty(), Empty(), Empty(), Pawn(Color.BLACK), Rook(Color.BLACK)],
            [Knight(Color.WHITE), Pawn(Color.WHITE), Empty(), Empty(), Empty(), Empty(), Pawn(Color.BLACK), Knight(Color.BLACK)],
            [Bishop(Color.WHITE), Pawn(Color.WHITE), Empty(), Empty(), Empty(), Empty(), Pawn(Color.BLACK), Bishop(Color.BLACK)],
            [Queen(Color.WHITE), Pawn(Color.WHITE), Empty(), Empty(), Empty(), Empty(), Pawn(Color.BLACK), Queen(Color.BLACK)],
            [King(Color.WHITE), Pawn(Color.WHITE), Empty(), Empty(), Empty(), Empty(), Pawn(Color.BLACK), King(Color.BLACK)],
            [Bishop(Color.WHITE), Pawn(Color.WHITE), Empty(), Empty(), Empty(), Empty(), Pawn(Color.BLACK), Bishop(Color.BLACK)],
            [Knight(Color.WHITE), Pawn(Color.WHITE), Empty(), Empty(), Empty(), Empty(), Pawn(Color.BLACK), Knight(Color.BLACK)],
            [Rook(Color.WHITE), Pawn(Color.WHITE), Empty(), Empty(), Empty(), Empty(), Pawn(Color.BLACK), Rook(Color.BLACK)]
        ]
