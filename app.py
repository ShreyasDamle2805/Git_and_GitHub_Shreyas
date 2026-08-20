import os
import json
from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# MongoDB connection
client = MongoClient(os.getenv("MONGO_URI"))
db = client["devops_db"]

collection = db["form_submissions"]
todo_collection = db["todo_items"]


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        role = request.form.get("role")

        if not name or not email or not role:
            return render_template("index.html", error="Please fill all fields.")

        data = {
            "name": name,
            "email": email,
            "role": role
        }

        collection.insert_one(data)

        return redirect(url_for("success"))

    return render_template("index.html")


@app.route("/success")
def success():
    return render_template("success.html")


@app.route("/api")
def get_api_data():
    with open("data.json", "r") as file:
        data = json.load(file)

    return jsonify(data)


@app.route("/submittodoitem", methods=["POST"])
def submit_todo_item():
    item_name = request.form.get("itemName")
    item_description = request.form.get("itemDescription")
    item_id = request.form.get("itemId")
    item_uuid = request.form.get("itemUUID")
    item_hash = request.form.get("itemHash")

    if not item_name or not item_description:
        return jsonify({
            "status": "error",
            "message": "Item name and description are required"
        }), 400

    data = {
        "itemName": item_name,
        "itemDescription": item_description,
        "itemId": item_id,
        "itemUUID": item_uuid,
        "itemHash": item_hash
    }

    result = todo_collection.insert_one(data)

    return jsonify({
        "status": "success",
        "message": "To-Do item submitted successfully",
        "itemId": str(result.inserted_id)
    })


if __name__ == "__main__":
    app.run(debug=True)