import json

from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)

posts = {
    0: {
        "id": 0,
        "upvotes": 1,
        "title": "zero_post",
        "link": "zero_post_link",
        "username": "zero_post_user",
        "comments": {
            0: {
                "id": 0,
                "upvotes": 8,
                "text": "0-0 comment",
                "username": "0-0 username"
            }, 
            1: {
                "id": 1,
                "upvotes": -14,
                "text": "0-1 comment",
                "username": "0-1 username"                
            }
        }
    },
    1: {
        "id": 1,
        "upvotes": 3,
        "title": "one_post",
        "link": "one_post_link",
        "username": "one_post_user", 
        "comments": {

        }       
    }
}

@app.route("/")
def hello_world():
    return "Hello world!"


# your routes here
@app.route("/api/posts/", methods=["GET"])
def get_posts():
    """
    Returns: Retrieve all posts
    """
    res = {"posts": list(posts.values())}
    return json.dumps(res), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
