from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin as sm

db = SQLAlchemy()


class User(db.Model, sm):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)

    def __repr__(self):
        return f'<User {self.username}>'