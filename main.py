from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:mypassword@localhost:5432/mydatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Define the Pyth_User model
class Pyth_User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, name, email):
        self.name = name
        self.email = email

# Create the database tables
with app.app_context():
    db.create_all()

# Define a DTO mapper for Pyth_User
class Pyth_UserDTO:
    def __init__(self, name, email):
        self.name = name
        self.email = email

# REST controller to create and store Pyth_User
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user_dto = Pyth_UserDTO(**data)
    new_user = Pyth_User(name=user_dto.name, email=user_dto.email)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
