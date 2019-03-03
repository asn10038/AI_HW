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
		"reams": 100,
        "id": 1
	},
	{
		"salesperson": "Stanley Hudson",
		"client": "Toast",
		"reams": 400,
        "id": 2
	},
	{
		"salesperson": "Michael G. Scott",
		"client": "Computer Science Department",
		"reams": 1000,
        "id": 3
	},
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



@app.route('/add_sale', methods=['GET', 'POST'])
def add_sale():
    global sales
    global current_sales_id

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
    except:
        print("LOGGING: invalid request to add_sale just returning the list")

    #send back the WHOLE array of sales, so the client can redisplay it
    return jsonify(data = sales)

@app.route('/delete_sale', methods=['GET', 'POST'])
def delete_sale():
    global sales
    id = request.get_json()['id']
    print(sales)
    for x in range(len(sales)):
        print(sales[x])
        if sales[x]['id'] == int(id):
            del sales[x]
            break
    return jsonify(data=sales)







if __name__ == '__main__':
   app.run(debug = True)
