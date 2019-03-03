import traceback
from flask import Flask
from flask import render_template
from flask import Response, request, jsonify
app = Flask(__name__)


current_id = 2

current_sales_id = 3
sales = [
	{
		"salesperson": "James D. Halpert",
		"client": "Shake Shack",
		"reams": 1000,
        "id": 1
	},
	{
		"salesperson": "Stanley Hudson",
		"client": "Toast",
		"reams": 4000,
        "id": 2
	},
	{
		"salesperson": "Michael G. Scott",
		"client": "Computer Science Department",
		"reams": 10000,
        "id": 3
	},
]

clients = [
    "Shake Shack",
    "Toast",
    "Computer Science Department",
    "Teacher's College",
    "Starbucks",
    "Subsconsious",
    "Flat Top",
    "Joe's Coffee",
    "Max Caffe",
    "Nussbaum & Wu",
    "Taco Bell"
]

non_ppc_people = [
"Phyllis",
"Dwight",
"Oscar",
"Creed",
"Pam",
"Jim",
"Stanley",
"Michael",
"Kevin",
"Kelly"
]

ppc_people = [
"Angela"
]

@app.route('/')
def hello_world():
   return 'Hello World'

@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

@app.route('/infinity')
def infinity(name=None):
    return render_template('infinity.html')

@app.route('/ppc')
def ppc(name=None):
    return render_template('ppc.html')

@app.route('/add_sale', methods=['GET', 'POST'])
def add_sale():
    global sales
    global current_sales_id
    global clients

    sale = request.get_json()
    try:
        name = sale['salesperson']
        client = sale['client']
        reams = sale['reams']

        # add new entry to array with
        # a new id and the name the user sent in JSON
        current_sales_id += 1
        new_id = current_id
        new_sale_entry = {
            "salesperson": name,
            "client": client,
            "reams": reams,
            "id":  current_sales_id
        }
        sales.append(new_sale_entry)
        if client not in clients:
            clients.append(client)
    except:
        print("LOGGING: invalid request to add_sale just returning the list")

    #send back the WHOLE array of sales, so the client can redisplay it
    return jsonify(data = {'sales':sales, 'clients':clients})

@app.route('/delete_sale', methods=['GET', 'POST'])
def delete_sale():
    global sales
    global clients
    id = request.get_json()['id']
    print(sales)
    for x in range(len(sales)):
        print(sales[x])
        if sales[x]['id'] == int(id):
            del sales[x]
            break
    return jsonify(data = {'sales':sales, 'clients':clients})

@app.route('/move_to_ppc', methods=['GET', 'POST'])
def move_to_ppc():
    global ppc_people
    global non_ppc_people
    try:
        name = request.get_json()['name']
        for x in range(len(non_ppc_people)):
            if non_ppc_people[x] == name:
                del non_ppc_people[x]
                break
        ppc_people.append(name)
    except:
        print("Move to ppc Illegal name movement ")
        traceback.print_exc()

    return jsonify(data={'ppc': ppc_people, 'non_ppc': non_ppc_people})

@app.route('/move_to_non_ppc', methods=['GET', 'POST'])
def move_to_non_ppc():
    global ppc_people
    global non_ppc_people
    try:
        name = request.get_json()['name']
        for x in range(len(ppc_people)):
            if ppc_people[x] == name:
                del ppc_people[x]
                break
        non_ppc_people.append(name)
    except:
        print("Move to ppc Illegal name movement " + name)
        traceback.print_exc()

    return jsonify(data={'ppc': ppc_people, 'non_ppc': non_ppc_people})


if __name__ == '__main__':
   app.run(debug = True)
