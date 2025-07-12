from app.extensions import db

class Quest(db.Model):
    id = db.Column(db.Integer)
    title = db.Column(db.String(150), primary_key=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    quest = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    response_to_wrong = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    
    def __repr__(self):
        return f'Quest {self.id}: {self.title} - {self.status}'