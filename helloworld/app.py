from chalice import Chalice
import json

app = Chalice(app_name='helloworld')

USERS = {}


# Example user in USERS:
# {
#     "some_username123": {
#         "username": "some_username123",
#         "age": 20
#     }
# }

@app.route("/")
def index():
    return {'hello': 'world'}


# CREATE (POST)
@app.route('/users', methods=['POST'])
def create_user():
    user_as_json = app.current_request.json_body
    USERS[user_as_json["username"]] = user_as_json
    return user_as_json


# READ (GET)
@app.route("/users", methods=["GET"])
def read_users():
    return json.dumps(USERS)


# READ (GET)
@app.route("/users/{username}", methods=["GET"])
def read_user(username):
    if username and username in USERS:
        return json.dumps(USERS[username])
    return {"error": f"'{username}' is not an existing user."}


# UPDATE (PUT)
@app.route("/users", methods=["PUT"])
def update_user():
    user_as_json = app.current_request.json_body
    USERS[user_as_json["username"]] = user_as_json
    return user_as_json


# DELETE (DELETE)
@app.route("/users", methods=["DELETE"])
def delete_user():
    user_as_json = app.current_request.json_body
    if user_as_json["username"] in USERS:
        del USERS[user_as_json["username"]]
    return user_as_json
