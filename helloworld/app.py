from chalice import Chalice
import json
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute

app = Chalice(app_name='helloworld')


# Define user model
class User(Model):
    class Meta:
        table_name = 'users_table'
        region = 'us-east-1'

    username = UnicodeAttribute(hash_key=True)
    age = NumberAttribute()


if not User.exists():
    User.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)


# CREATE (POST)
@app.route('/users', methods=['POST'])
def create_user():
    user_as_json = app.current_request.json_body
    user = User(username=user_as_json["username"], age=user_as_json["age"])
    user.save()
    return user_as_json


# READ (GET)
@app.route("/users", methods=["GET"])
def read_users():
    users = User.scan()
    user_data = []
    for user in users:
        user_data.append({
            "username": user.username,
            "age": user.age
        })
    return json.dumps(user_data)


# READ (GET)
@app.route("/users/{username}", methods=["GET"])
def read_user(username):
    try:
        user = User.get(username)
        return {
            "username": user.username,
            "age": user.age
        }
    except User.DoesNotExist:
        return {"error": f"'{username}' is not an existing user."}


# UPDATE (PUT)
@app.route("/users", methods=["PUT"])
def update_user():
    user_as_json = app.current_request.json_body
    try:
        user = User.get(user_as_json["username"])
        user.age = user_as_json["age"]
        user.save()  # update user
        return user_as_json
    except User.DoesNotExist:
        return {"error": f"'{user_as_json['username']}' is not an existing user."}


# DELETE (DELETE)
@app.route("/users", methods=["DELETE"])
def delete_user():
    user_as_json = app.current_request.json_body
    try:
        user = User.get(user_as_json["username"])
        user.delete()  # deletes user
        return user_as_json
    except User.DoesNotExist:
        return {"error": f"'{user_as_json['username']}' is not an existing user."}
