import json
from flask import Flask, request
import db

DB = db.DatabaseDriver()

app = Flask(__name__)


@app.route("/")
def hello_world():
    """
    """
    return "Hello world!"


# your routes here
@app.route("/api/users/", methods=["GET"])
def get_users():
    """
    Endpoint that returns json with all user's information
    """
    users = DB.select_users()
    return json.dumps({"users": users}), 200

@app.route("/api/users/", methods=["POST"])
def create_user():
    """
    Endpoint returns json of information on newly created user and 
    success code 201
    """
    # fetch body information
    body = json.loads(request.data)
    # check if name and username is valid, otherwise return 400
    if body["name"] and body["username"]:
        balance = body.get("balance", 0)
        #call method to insert user into users data, and get id of new user
        user_id = DB.insert_user(body["name"], body["username"], balance)

        if user_id is None:
            return json.dumps({"error": "Error occured while creating task"}), 400
        return json.dumps(DB.select_user_id(user_id)), 201

    return json.dumps({"error": "Name and/or username missing"}), 400



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
