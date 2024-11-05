import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from modules import db, User, RequestLog
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Використовуємо змінну середовища DATABASE_URL для підключення до бази даних
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Альтернативний спосіб створення таблиць
with app.app_context():
    db.create_all()

# Маршрут для отримання всіх членів родини
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

# Маршрут для отримання конкретного члена родини за ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

# Маршрут для додавання нового члена родини
@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    new_user = User(
        name=data['name'],
        age=data.get('age'),
        gender=data.get('gender'),
        parent_id=data.get('parent_id')
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 201

# Маршрут для оновлення інформації про члена родини
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    user.name = data.get('name', user.name)
    user.age = data.get('age', user.age)
    user.gender = data.get('gender', user.gender)
    db.session.commit()
    return jsonify(user.to_dict())

# Маршрут для видалення члена родини
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"})

# Маршрут для логування запитів
@app.before_request
def log_request():
    log = RequestLog(
        method=request.method,
        path=request.path,
        ip=request.remote_addr
    )
    db.session.add(log)
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
