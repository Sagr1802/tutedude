from flask import Flask, jsonify, render_template, request, redirect, url_for
import json
import pymongo
from pymongo.errors import PyMongoError

app = Flask(__name__)

# MongoDB Atlas connection
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

# Route 2: Form submission (UI)
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

# Route 3: Success page
@app.route('/success')
def success():
    return render_template('success.html')

# ✅ NEW Route 4: Submit To-Do item via JSON API
@app.route('/submittodoitem', methods=['POST'])
def submit_todo_item():
    try:
        data = request.get_json()
        item_name = data.get('itemName')
        item_desc = data.get('itemDescription')

        if not item_name or not item_desc:
            return jsonify({"error": "Missing itemName or itemDescription"}), 400

        collection.insert_one({
            "itemName": item_name,
            "itemDescription": item_desc
        })

        return jsonify({"message": "Item submitted successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Main entry
if __name__ == '__main__':
    app.run(debug=True)
