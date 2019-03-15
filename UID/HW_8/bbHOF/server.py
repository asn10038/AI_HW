import traceback
from flask import Flask
from flask import render_template
from flask import Response, request, jsonify
import json
from pprint import pprint

app = Flask(__name__)

DATA_FILE = '../players2.json'
PLAYER_DATA = []
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
    if request.method == 'POST':
        results = search_info(request.get_json())
        return jsonify(data={'players' : results})
    return render_template('search.html')

@app.route('/view_item/<id>')
def view_item(id=3):
    player = get_player(id)
    try:
        return render_template('view_item.html', id=id,
                                fullname=player['full_name'],
                                born=player['born'],
                                image_url=player['image_url'],
                                bio=player['bio'],
                                rookie_status=player['rookie_status'],
                                last_game=player['last_game'],
                                positions=player['positions'],
                                throws=player['throws'],
                                bats=player['bats'],
                                WAR=player['WAR'])
    except:
        return render_template('add-item.html', positions=POSITIONS)

def add_player(player):
    global current_id
    player['id'] = current_id
    current_id +=1
    PLAYER_DATA.append(player)
    pprint(player)
    return player['id']

def get_player(id):
    for player in PLAYER_DATA:
        if player['id'] == int(id):
            return player
    print("COULDNT FIND PLAYER")
    return None

def load_players():
    global PLAYER_DATA
    PLAYER_DATA=json.load(open(DATA_FILE))

def search_info(query):
    res = []
    ids = set()
    str_q = str(query)
    for player in PLAYER_DATA:
        for field in player:
            if field != 'image_url' and field != 'id' and query.upper() in str(player[field]).upper() and player['id'] not in ids:
                res.append(player)
                ids.add(player['id'])
    pprint(res)
    return res

if __name__ == '__main__':
    load_players()
    app.run(debug = True)
