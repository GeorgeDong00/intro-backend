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
                "username": "0-0 username",
                "comments": {}
            }, 
            1: {
                "id": 1,
                "upvotes": -14,
                "text": "0-1 comment",
                "username": "0-1 username",
                "comments": {}                
            }
        }
    },
    1: {
        "id": 1,
        "upvotes": 3,
        "title": "one_post",
        "link": "one_post_link",
        "username": "one_post_user", 
        "comments": {}       
    }
}

post_id_counter = 2
comment_id_counter = 2

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

@app.route("/api/posts/", methods=["POST"])
def create_post():
    """
    Returns json of created post with status 201

    Parameter request.body: json containing body of created post
    Precondition: request body contains title, link, username values
    """
    global post_id_counter
    body = json.loads(request.data)

    if body["title"] and body["link"] and body["username"]:

        new_post = {
            "id": post_id_counter,
            "upvotes": 1,
            "title": body["title"],
            "link": body["link"],
            "username": body["username"], 
            "comments": {}   
        }

        posts[post_id_counter] = new_post
        post_id_counter += 1
        return json.dumps(new_post), 201

    return json.dumps({"error": "new post was not created"}), 400

@app.route("/api/posts/<int:post_id>/", methods=["GET"])
def get_post(post_id):
    """
    Returns json of post_id post with status 200

    Parameter post_id: id of specific post 
    Precondition: post_id must exist in posts dict
    """
    if post_id not in posts:
        return json.dumps({"error": "post doesn't exist"}), 404    
    res = post_data(post_id)
    return json.dumps(res), 200

@app.route("/api/posts/<int:post_id>/", methods=["DELETE"])
def delete_post(post_id):
    """
    Returns json of deleted post with status 200

    Parameter post_id: id of specific post 
    Precondition: post_id must exist in posts dict
    """
    if post_id not in posts:
        return json.dumps({"error": "post doesn't exist"}), 404
    res = post_data(post_id)
    del posts[post_id]
    return json.dumps(res), 200

@app.route("/api/posts/<int:post_id>/comments/", methods=["GET"])
def get_comments(post_id):
    """
    Returns json of post's comment(s) with status 200

    Parameter post_id: id of specific post 
    Precondition: post_id must exist in posts dict
    """
    if post_id not in posts:
        return json.dumps({"error": "post doesn't exist"}), 404
    data = posts[post_id]
    return json.dumps({"comments": list(data["comments"].values())}), 200


@app.route("/api/posts/<int:post_id>/comments/", methods=["POST"])
def create_comment(post_id):
    """
    Returns json of created post's comment(s) with status 201

    Parameter post_id: id of specific post 
    Precondition: post_id must exist in posts dict

    Parameter request.body: body containing comment's information
    Precondition: request.body must have text and username value
    """
    if post_id not in posts:
        return json.dumps({"error": "post doesn't exist"}), 404
    
    # fetch global variable
    global comment_id_counter
    # fetch request body
    body = json.loads(request.data)

    if body["text"] and body["username"]:
        # extract post's comments dictionary
        data = posts[post_id]
        comment_dict = data["comments"]
        # create a dictionary
        new_comment = {
            "id": comment_id_counter,
            "upvotes": 1,
            "text": body["text"],
            "username": body["username"],
            "comments": {}
        }
        # set comments[comment_id] to created dictionary
        comment_dict[comment_id_counter] = new_comment
        #increment global variable comment
        comment_id_counter += 1
        # return json of newly created comment
        return json.dumps(new_comment), 201
    
    return json.dumps({"error": "comment was not posted"})

@app.route("/api/posts/<int:post_id>/comments/<int:comment_id>/", methods=["POST"])
def edit_comment(post_id, comment_id):
    """
    Returns json of edited comment with status 200

    Parameter post_id: id of specific post 
    Precondition: post_id must exist in posts dict

    Parameter comment_id: id of specific comment 
    Precondition: comment_id must exist in post's comment's key

    Parameter request.body: body containing new text for comment
    Precondition: request.body must contain text
    """
    if post_id not in posts:
        return json.dumps({"error": "post doesn't exist"}), 404
    
    #validate request body has text
    body = json.loads(request.data)

    if body["text"]:
        #fetch post's comments dictionary
        data = posts[post_id]
        comment_dict = data["comments"]
        
        #validate comment_id existent in comment's dictionary key
        if comment_id in comment_dict:
            edit_comment = comment_dict[comment_id]
            #set comment_id's key to request body's value
            edit_comment["text"] = body["text"]
            #create dictionary to be return
            res = {
                "id": edit_comment["id"],
                "upvotes": edit_comment["upvotes"],
                "text": edit_comment["text"],
                "username": edit_comment["username"]
            }
            #return json newly created dictionary
            return json.dumps(res), 200

        return json.dumps({"errors": "comment doesn't exist"}), 404

    return json.dumps({"errors": "comment was not updated"}),404

#helper functions below
def post_data(id):
    """
    Return a dictionary of id's specified post

    Parameter id: id of specific post 
    Precondition: id must exist in posts dict
    """
    data = posts[id]
    return {
        "id": data["id"],
        "upvotes": data["upvotes"],
        "title": data["title"],
        "link": data["link"],
        "username": data["username"]
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    
