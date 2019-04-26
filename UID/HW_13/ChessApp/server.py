import traceback
from flask import Flask
from flask import render_template
from flask import Response, request, jsonify
import json
from pprint import pprint
from flask import send_from_directory
import chess
import chess.pgn
import models
app = Flask(__name__)

GAMES = {}

@app.route('/')
def hello_world():
   return 'Hello World'

@app.route('/games/<id>')
def games(id=None):
    pgn = GAMES[id]
    try:
        print(request.args)
        if 'quiz' not in request.args:
            return render_template('view-game.html', pgn=str(pgn) )
        else:
            return render_template('quiz-game.html', pgn=str(pgn))
    except KeyError:
        return render_template('view-game.html', pgn=str(pgn) )

@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

@app.route('/games/img/<path:path>')
def send_img(path):
    return send_from_directory('static/img', path)

@app.route('/games/home')
def index():
    info = get_game_info()
    return render_template('index.html', games=info)

def load_games():
    global GAMES
    with open('/home/ant/GRAD_HW/UID/HW_11/chess_media/RobertJamesFischer.pgn') as pgn:
        for x in range(50):
            GAMES[str(x)] = chess.pgn.read_game(pgn)

def get_game_info():
    for game in GAMES:
        id=game
        event = GAMES[game].headers['Event']
        white_player = GAMES[game].headers['White']
        black_player = GAMES[game].headers['Black']
        site = GAMES[game].headers['Site']
        date = GAMES[game].headers['Date']
        yield models.GameSummary(id=id, event=event, white_player=white_player,
                                 black_player=black_player, site=site, date=date)

if __name__ == '__main__':
    load_games()
    app.run(debug = True)
