from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# Модель для представлення користувача (члена родини)
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    parent_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # Зв'язок між користувачами для дітей
    children = db.relationship(
        "User", 
        backref=db.backref('parent', remote_side=[id]), 
        lazy=True
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "parent_id": self.parent_id,
            "children": [child.id for child in self.children]
        }

# Модель для логування запитів до сервера
class RequestLog(db.Model):
    __tablename__ = 'request_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    method = db.Column(db.String(10))
    path = db.Column(db.String(100))
    ip = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "method": self.method,
            "path": self.path,
            "ip": self.ip,
            "timestamp": self.timestamp.isoformat()
        }
