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
    Returns json containing all post with status 200
    """
    res = {"posts": list(posts.values())}
    return json.dumps(res), 200

@app.route("/app/posts/", methods=["POST"])
def create_post():
    """
    Returns json of created post with status 201

    Parameter body: json containing information of created post
    Precondition: json contains title, link, username values
    """
    pass

@app.route("/api/posts/<int:post_id/>", methods=["GET"])
def get_post():
    """
    Returns json of post_id post with status 200

    Parameter post_id: id of specific post 
    Precondition: post_id must exist in posts dict
    """
    pass

@app.route("/api/posts/<int:post_id>/", methods=["DELETE"])
def delete_post():
    """
    Returns json of deleted post with status 200

    Parameter post_id: id of specific post 
    Precondition: post_id must exist in posts dict
    """
    pass

@app.route("/api/posts/<int:post_id>/comments/", methods=["GET"])
def get_comments():
    """
    Returns json of post's comment(s) with status 200

    Parameter post_id: id of specific post 
    Precondition: post_id must exist in posts dict
    """
    pass

@app.route("/api/posts/<int:post_id>/comments/", methods=["POST"])
def create_comments():
    """
    Returns json of created post's comment(s) with status 201

    Parameter post_id: id of specific post 
    Precondition: post_id must exist in posts dict
    """
    pass

@app.route("/api/posts/<int:post_id>/comments/<int:comment_id/>", methods=["POST"])
def edit_comments():
    """
    Returns json of edited comment with status 200

    Parameter post_id: id of specific post 
    Precondition: post_id must exist in posts dict

    Parameter comment_id: id of specific comment 
    Precondition: comment_id must exist in post's comment's key
    """
    pass

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
