from models import User, db
from app import app, bcrypt
from faker import Faker

fake = Faker()

with app.app_context():
    
    print("Deleting all records...")
    User.query.delete()
    
    print("Creating users...")
    users = []
    for _ in range(5):
        
        raw_password = fake.password(length=6, special_chars=True, digits=True, upper_case=True, lower_case=True)
        hashed_password = bcrypt.generate_password_hash(raw_password).decode('utf-8')
        
        user = User(
            username = fake.name(),
            password = hashed_password
        )
        
        users.append(user)
    db.session.add_all(users)
    db.session.commit()
    print("Complete.")