from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import pymongo
from urllib.parse import quote_plus
import certifi

load_dotenv()
MONGO_USERNAME = os.getenv("USER_NAME")
MONGO_PASSWORD = os.getenv("USER_PASSWORD")

MONGO_URL = f"mongodb+srv://{quote_plus(MONGO_USERNAME)}:{quote_plus(MONGO_PASSWORD)}@flask-test-data.l0grk7f.mongodb.net/"
print("MongoDB URL:", MONGO_URL)
client= pymongo.MongoClient(MONGO_URL, tlsCAFile=certifi.where())
print("MongoDB Client:", client)
db=client['flask-test']
collection=db['users']
app = Flask(__name__)

@app.route('/')
def home():
    return "Home page accessed"

@app.route('/signup')
def signup():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    form_data= dict(request.form)
    collection.insert_one(form_data)
    return f"Submitted data: {form_data}"

@app.route('/view')
def view():
    all_data = list(collection.find())
    return f"Viewing all data: {all_data}"

@app.route('/api/<name>')
def api(name):
    #http://127.0.0.1:5000/api/rohit
    return f"API accessed with name: {name}"

@app.route('/add/<int:a>/<int:b>')
def add(a, b):
    #http://127.0.0.1:5000/add/4/5
    return f"Sum of {a} and {b} is {a + b}"

@app.route('/api/data')
def api_data():
    #http://127.0.0.1:5000/api/data?name=rohit&age=26&city=dombivali
    name = request.args.get('name', 'Guest')
    age = request.args.get('age', 'Unknown')
    city = request.args.get('city', 'Unknown')
    data = {
        "name": name,
        "age": age,
        "city": city
    }
    return data
if __name__ == '__main__':    app.run(debug=True)