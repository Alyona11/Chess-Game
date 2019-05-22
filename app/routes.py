from flask import render_template, request, jsonify

from app import app
from app.chessboard import Chessboard

chessboard = Chessboard()  # Об'єкт типу Chessboard для виклику методів класу Chessboard


@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():  # Спрацьовує при виклику localhost:5000/ або localhost:5000/home з методом GET
    games = chessboard.get_games()
    return render_template('index.html', games=games)  # Повертає HTML-сторінку templates/index.html з параметром games


@app.route('/game', methods=['GET'])
def game():  # Спрацьовує при виклику localhost:5000/game з методом GET
    return render_template('chessboard.html', board=chessboard.board)  # Повертає HTML-сторінку templates/chessboard.html з параметром board об'єкта класа chessboard


@app.route('/targets', methods=['POST'])
def targets():  # Спрацьовує при виклику localhost:5000/targets з методом POST
    current_position = request.form['position']  # Взяти з реквеста інформацію про позицію фігури, якою хочуть зробити хід
    if chessboard.is_piece_allowed(current_position):  # Перевірити, чи гравець ходить своєю фігурою
        target_positions = chessboard.get_targets_of_unparsed_position(current_position)  # Вирахувати всі можливі ходи
        return jsonify(targets=target_positions)  # Повернути клієнту всі можливі ходи
    else:
        return jsonify('Piece is forbidden for current player'), 400  # Повернути клієнту повідмлення про помилку. Хід не своєю фігурою


@app.route('/movement', methods=['POST'])
def movement():  # Спрацьовує при виклику localhost:5000/movement з методом POST
    current_position = request.form['position']  # Взяти з реквеста інформацію про позицію фігури, якою хочуть зробити хід
    target_position = request.form['target']  # Взяти з реквеста інформацію про позицію, куди хочуть зробити хід

    is_check_for_next_player = chessboard.perform_movement(current_position, target_position)  # Зробити хід і перевірити чи виник шах
    if is_check_for_next_player:
        is_checkmate_for_next_player = chessboard.is_checkmate_for_current_player()  # Перевірити чи виник мат
        return jsonify(isCheck=is_check_for_next_player, isCheckmate=is_checkmate_for_next_player)  # Повернути клієнту інформацію про результат ходу
    else:
        return jsonify(isCheck=is_check_for_next_player, isCheckmate=False)  # Повернути клієнту інформацію про результат ходу


@app.route('/home', methods=['POST'])
def save():  # Спрацьовує при виклику localhost:5000/home з методом POST
    game_name = request.form['gameName']  # Взяти з реквеста назву гри яку хочуть зберегти
    chessboard.save_game(game_name)  # Зберегти гру
    games = chessboard.get_games()  # Взяти з бази даних всі збережені ігри для відображення на стартовій сторінці
    return render_template('index.html', games=games)  # Повертає HTML-сторінку templates/index.html з параметром games


@app.route('/new', methods=['POST'])
def new_game():  # Спрацьовує при виклику localhost:5000/new з методом POST
    chessboard.clear_board()
    return jsonify(success=True)  # Повернути клієнту інформацію про успішне створення нової гри


@app.route('/replay', methods=['GET'])
def replay():  # Спрацьовує при виклику localhost:5000/replay з методом GET
    game_name = request.args.get('game')  # Взяти з реквеста інформацію про назву гри, яку хочуть відтворити
    game_activity = chessboard.get_game_activity(game_name)  # Взфти з бази даних інформацію про ходи збереженої гри
    return jsonify(activity=game_activity)  # Повернути клієнту інформацію про ходи збереженої гри
