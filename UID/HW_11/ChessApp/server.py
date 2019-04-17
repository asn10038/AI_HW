import traceback
from flask import Flask
from flask import render_template
from flask import Response, request, jsonify
import json
from pprint import pprint
from flask import send_from_directory
import chess
import chess.pgn
app = Flask(__name__)

GAMES = {}

@app.route('/')
def hello_world():
   return 'Hello World'

@app.route('/games/<id>')
def games(id=None):
    pgn = GAMES[id]
    return render_template('view-game.html', pgn=str(GAMES[id]) )

@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

@app.route('/games/img/<path:path>')
def send_img(path):
    return send_from_directory('static/img', path)

def load_games():
    global GAMES
    with open('/home/ant/GRAD_HW/UID/HW_11/chess_media/RobertJamesFischer.pgn') as pgn:
        for x in range(50):
            GAMES[str(x)] = chess.pgn.read_game(pgn)

if __name__ == '__main__':
    load_games()
    app.run(debug = True)
