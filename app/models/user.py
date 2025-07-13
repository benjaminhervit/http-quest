from app.extensions import db

class User(db.Model):
    id = db.Column('id',db.Integer, primary_key=True)
    username = db.Column('username',db.String(31), nullable=False)
    
    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def get_by_id(cls, user_id):
        return cls.query.get(user_id)
    
    def __repr__(self):
        return f'<User {self.id}, {self.username}>'
    