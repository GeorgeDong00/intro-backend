import json
from flask import Flask, request
import db
import hashlib

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
    Endpoint creates new user using request body information containing name,
    username and optional balance amount (otherwise 0).
    
    Returns json of information on newly created user and success code 201. 
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

@app.route("/api/user/<int:user_id>/", methods=["GET"])
def get_user(user_id):
    """
    Endpoint fetches user of specified id. 

    Returns json of user's information if successful.
    """
    user_data = DB.select_user_id(user_id)
    if user_data is not None:
        return json.dumps(DB.select_user_id(user_id)), 201
    return json.dumps({"error": "User doesn't exist"}), 404

@app.route("/api/user/<int:user_id>/", methods=["DELETE"])
def delete_user(user_id):
    """
    Endpoint deletes user of specified id.

    Returns json of deleted user's information if successful. 
    """
    del_user = DB.select_user_id(user_id)
    if not del_user:
        return json.dumps({"error": "User doesn't exist"}), 404
    DB.delete_user(user_id)
    return json.dumps(del_user), 200
    
@app.route("/api/send/", methods=["POST"])
def send_money():
    """
    Endpoint that accepts a request with sender's id, receiver's id and 
    transfer amount and initiates the transaction.
    
    Returns request body of transaction process if successful.
    """
    # validate sender_id, receiver_id, amount parameter are filled
    body = json.loads(request.data)
    if body["sender_id"] and body["receiver_id"] and body["amount"]: 

        sender = body.get("sender_id")
        receiver = body.get("receiver_id")
        amount = body.get("amount")

        # validate sender_id and receiver_id exist in database
        sender_data = DB.select_user_id(sender)
        receiver_data = DB.select_user_id(receiver)

        if sender_data and receiver_data:
            # validate sender's balance exceeds amount being sent
            if sender_data[0]["balance"] >= body["amount"]:

                # deduct sender_id's balance by amount
                send_bal = sender_data[0]["balance"] - amount
                DB.update_bal(sender, send_bal)

                # increase receiver_id's balance by amount
                receiver_bal = receiver_data[0]["balance"] + amount
                DB.update_bal(receiver, receiver_bal)

                #return json of transaction
                return json.dumps(body), 200

            return json.dumps({"error": "Sender's amount exceed balance"}), 400
        return json.dumps({"error": "Sender and/or receiver doesn't exist"}), 404
    return json.dumps({"error": "Missing sender, receiver, and/or transaction amount"}), 400

# optional challenges
@app.route("/api/extra/users/", methods=["POST"])
def create_user_secured():
    """
    Endpoint creates new secured user using request body information containing name,
    username, optional balance amount (otherwise 0) and password.
    
    Returns json of information on newly created user and success code 201. 
    """
    # fetch body information
    body = json.loads(request.data)
    # check if name and username is valid, otherwise return 400
    if body["name"] and body["username"] and body["password"]:
        balance = body.get("balance", 0)
        #call method to insert user into users data, and get id of new user
        user_id = DB.insert_user(body["name"], body["username"], balance, body["password"])

        if user_id is None:
            return json.dumps({"error": "Error occured while creating task"}), 400
        return json.dumps(DB.select_user_id(user_id)), 201

    return json.dumps({"error": "Name, username, and/or password missing"}), 400

@app.route("/api/extra/user/<int:user_id>/", methods=["POST"])
def get_secured_user(user_id):
    """
    Endpoint fetches user of specified id if password input matches with database.
    Returns json of user's information if successful.

    Parameter user_id: id of user
    Precondition user_id must be an id of an user with valid password that isn't default None
    """
    body = json.loads(request.data)
    if body.get("password"): 

        user_data = DB.select_user_id(user_id)
        if user_data is not None:

            if valid_pass(user_id, body["password"]):
                return json.dumps(DB.select_user_id(user_id)), 201

            return json.dumps({"error": "Password is incorrect"}), 401
        return json.dumps({"error": "User doesn't exist"}), 404
    return json.dumps({"error": "Error occured while accessing password"}), 400

@app.route("/api/extra/send/", methods=["POST"])
def send_money_secured():
    """
    Endpoint that accepts a request with sender's id, receiver's id, 
    transfer amount, and sender's password prior to initiating the transaction.
    
    Returns json of transaction process if successful.
    """
    # validate sender_id, receiver_id, amount parameter are filled
    body = json.loads(request.data)
    if body["sender_id"] and body["receiver_id"] and body["amount"]: 

        sender = body.get("sender_id")
        receiver = body.get("receiver_id")
        amount = body.get("amount")
        
        #validate sender's password exist and matches with database
        if body["sender_password"] and valid_pass(sender, body["sender_password"]):
            # validate sender_id and receiver_id exist in database
            sender_data = DB.select_user_id(sender)
            receiver_data = DB.select_user_id(receiver)

            if sender_data and receiver_data:
                # validate sender's balance exceeds amount being sent
                if sender_data[0]["balance"] >= body["amount"]:

                    # deduct sender_id's balance by amount
                    send_bal = sender_data[0]["balance"] - amount
                    DB.update_bal(sender, send_bal)

                    # increase receiver_id's balance by amount
                    receiver_bal = receiver_data[0]["balance"] + amount
                    DB.update_bal(receiver, receiver_bal)

                    #return json of transaction
                    return json.dumps({"sender_id": sender, "reciever_id": receiver, "amount": amount}), 200

                return json.dumps({"error": "Sender's amount exceed balance"}), 400
            return json.dumps({"error": "Sender and/or receiver doesn't exist"}), 404
        return json.dumps({"error": "Password is incorrect or not sent"}), 401
    return json.dumps({"error": "Missing sender, receiver, and/or transaction amount"}), 400


# helper function
def valid_pass(user_id, password):
    """
    """
    if password == DB.select_password(user_id)[0]["password"]:
        return True
    return False


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
