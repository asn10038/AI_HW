import traceback
from flask import Flask
from flask import render_template
from flask import Response, request, jsonify
import json
from pprint import pprint

app = Flask(__name__)

DATA_FILE = '../players2.json'
PLAYER_DATA = json.load(open(DATA_FILE))
current_id = 100

POSITIONS = ["Catcher", "Pitcher", "Designated Hitter", "Centerfielder", "Rightfielder",
             "Leftfielder", "First Baseman", "Second Baseman", "Third Baseman", "Shortstop", "Outfielder" ]


@app.route('/')
def hello_world():
   return 'Hello World'

@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        new_id = add_player(request.get_json())
        return jsonify(data={'link-to-view' : '/view_item/'+str(new_id)})

    return render_template('add-item.html', positions=POSITIONS)

@app.route('/search', methods=['GET', 'POST'])
def search():
	return render_template('search.html')

@app.route('/view_item/<id>')
def view_item(id=3):
	return render_template('view_item.html', id=id)

def add_player(player):
    global current_id
    player['id'] = current_id
    current_id +=1
    PLAYER_DATA.append(player)
    return player['id']


if __name__ == '__main__':
   app.run(debug = True)
