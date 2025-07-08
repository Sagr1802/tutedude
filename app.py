from flask import Flask, jsonify, render_template, request, redirect, url_for
import json
import pymongo
from pymongo.errors import PyMongoError

app = Flask(__name__)

#  MongoDB Atlas connection
client = pymongo.MongoClient("mongodb+srv://root:admin@admin.yq76s45.mongodb.net/?retryWrites=true&w=majority")
db = client['Myapp']
collection = db['myCollection'] 

# Route 1: Return JSON list from file
@app.route('/api')
def api():
    try:
        with open('data.json') as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404

#  Route 2: Form page
@app.route('/', methods=['GET', 'POST'])
def form():
    error = None
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        try:
            collection.insert_one({'name': name, 'age': int(age)})
            return redirect(url_for('success'))
        except PyMongoError as e:
            error = str(e)
    return render_template('form.html', error=error)

#  Success page
@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)
