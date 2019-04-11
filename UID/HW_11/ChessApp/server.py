import traceback
from flask import Flask
from flask import render_template
from flask import Response, request, jsonify
import json
from pprint import pprint
from flask import send_from_directory
app = Flask(__name__)


@app.route('/')
def hello_world():
   return 'Hello World'

@app.route('/games')
def games():
    return render_template('view-game.html')

@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

@app.route('/img/<path:path>')
def send_img(path):
    return send_from_directory('static/img', path)



if __name__ == '__main__':
    app.run(debug = True)
