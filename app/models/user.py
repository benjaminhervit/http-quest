from app.extensions import db

class User(db.Model):
    id = db.Column(db.String(4,20), primary=True)
    
    def __repr__(self):
        return f'<User {self.id}>'
    