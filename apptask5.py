from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage for user data
users = {
    1: {"id": 1, "name": "Alice", "email": "alice@example.com"},
    2: {"id": 2, "name": "Bob", "email": "bob@example.com"}
}
next_id = 3

# GET all users
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(list(users.values()))

# GET a single user by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

# POST a new user
@app.route('/users', methods=['POST'])
def create_user():
    global next_id
    data = request.get_json()
    if not data.get("name") or not data.get("email"):
        return jsonify({"error": "Missing name or email"}), 400
    user = {"id": next_id, "name": data["name"], "email": data["email"]}
    users[next_id] = user
    next_id += 1
    return jsonify(user), 201

# PUT to update a user
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = users.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    data = request.get_json()
    user["name"] = data.get("name", user["name"])
    user["email"] = data.get("email", user["email"])
    return jsonify(user)

# DELETE a user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id in users:
        del users[user_id]
        return jsonify({"message": "User deleted"})
    return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
