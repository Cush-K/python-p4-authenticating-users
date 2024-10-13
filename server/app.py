from flask import Flask, make_response, jsonify, request, session
from models import db, User
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Resource, Api
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False
app.secret_key = os.urandom(24)

migrate = Migrate(app,db)
api = Api(app)
bcrypt = Bcrypt(app)
CORS(app)

db.init_app(app)


class Login(Resource):
    def post(self):
        user = User.query.filter_by(username = request.json['username']).first()
        
        password = str(request.json.get('password'))
            
        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
        
            return {
                "message": "Logged in successfully"    
                }, 200
        return {
            "message": "Invalid Credentials!"
        }, 401
        
api.add_resource(Login, '/login')
        
        
class Signup(Resource):
    def post(self):
            username = request.json.get('username')
            password = request.json.get('password')
            
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            
            new_user = User(username = username, password = hashed_password)
            
            db.session.add(new_user)
            db.session.commit()
            
            return make_response(new_user.to_dict(), 200)
    

api.add_resource(Signup, '/signup')

class CheckSession(Resource):

    def get(self):
        user = User.query.filter(User.id == session.get('user_id')).first()
        if user:
            return user.to_dict(), 200
        else:
            return {'message': '401: Not Authorized'}, 401

api.add_resource(CheckSession, '/check_session')

class Logout(Resource):

    def delete(self): # just add this line!
        session['user_id'] = None
        return {'message': '204: No Content'}, 204

api.add_resource(Logout, '/logout')

        


if __name__ == '__main__':
    app.run(port=5555, debug=True)