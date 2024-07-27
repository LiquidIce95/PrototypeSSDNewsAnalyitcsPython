from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:mypassword@localhost:5432/mydatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Define the Pyth_User model
class appUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, name, username):
        self.name = name
        self.username = username

# Create the database tables
with app.app_context():
    db.create_all()

# Define a DTO mapper for Pyth_User
class appUserDTO:
    def __init__(self, name, username):
        self.name = name
        self.username = username

# REST controller to create and store Pyth_User
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user_dto = appUserDTO(**data)
    new_user = appUser(user_dto.name, user_dto.username)
    db.session.add(new_user)
    db.session.commit()
    userId = new_user.id
    return jsonify({'message': 'User created successfully', 'userId': userId}), 201

# REST controller to delete a user by userID
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = appUser.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'}), 200
    else:
        return jsonify({'message': 'User not found'}), 404

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
