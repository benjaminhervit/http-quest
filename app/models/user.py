from app.extensions import db

class User(db.Model):
    id = db.Column('id',db.Integer, primary_key=True)
    username = db.Column('username',db.String(31), nullable=False)
    
    def __repr__(self):
        return f'<User {self.id}, {self.username}>'
    