# Rules of a REST API
# 1. Data is transferred as key value pairs called JSON
# Sending from JS as JSON objects -From python as dictionary
# 2.You must define routes/URL
# 3.You must define a http metthod. E.g-GET,POST,PUT,DELETE,PATCH
# 4.You must define a status code E.g-200,201,404,401,500
from flask import Flask, jsonify, request

app = Flask(__name__)

allowed_methods = ["GET", "POST", "PUT", "DELETE"]
user_list = []


@app.route('/', methods=allowed_methods)
def home():
    method = request.method.lower()
    if method == "get":
        return jsonify({"Flask APi Version": "1.0"}), 200
    else:
        return jsonify({"msg": "Method not allowed"}), 405


@app.route("/users", methods=allowed_methods)
def users():
    try:
        method = request.method.lower()
        if method == "get":
            return jsonify({"data": user_list}), 200
        elif method == "post":
            data = request.get_json()
            if data["name"] == "" or data["location"] == "":
                return jsonify({"msg": "All fields required"}), 401
            else:
                user_list.append(data)
                return jsonify({"msg": "Successfully added user"}), 201
        else:
            return jsonify({"msg": "Method not allowed"}), 405
    except Exception as e:
        return jsonify({"error":str(e)}),500

app.run(debug=True)
