import os
import json
import re
from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "default-key")

# Connect to MongoDB Atlas using environment variable
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
db = client["devops_db"]
collection = db["form_submissions"]

# Helper function: Validate email format using regex
def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        role = request.form.get('role')

        # Basic input validation
        if not name or not email or not role:
            return render_template('index.html', error="All fields are required!")

        # Email format validation
        if not is_valid_email(email):
            return render_template('index.html', error="Please enter a valid email address!")

        # Insert document into MongoDB Atlas
        try:
            document = {"name": name, "email": email, "role": role}
            collection.insert_one(document)
            return redirect(url_for('success'))
        except Exception as e:
            return render_template('index.html', error=f"Database error: {str(e)}")

    return render_template('index.html')

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/api', methods=['GET'])
def get_api_data():
    try:
        with open('data.json', 'r') as file:
            data = json.load(file)
        return jsonify(data)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/submittodoitem', methods=['POST'])
def submit_todo_item():
    item_name = request.form.get('itemName')
    item_description = request.form.get('itemDescription')

    if not item_name or not item_description:
        return jsonify({
            "status": "error",
            "message": "itemName and itemDescription are required"
        }), 400

    try:
        todo_collection = db["todo_items"]

        document = {
            "itemName": item_name,
            "itemDescription": item_description
        }

        result = todo_collection.insert_one(document)

        return jsonify({
            "status": "success",
            "message": "To-Do item submitted successfully",
            "itemId": str(result.inserted_id)
        }), 201

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == '__main__':
    app.run(debug=True)