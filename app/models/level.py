from app.extensions import db

class LevelModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    welcome_text = db.Column(db.Text)
    description = db.Column(db.Text)
    quest = db.Column(db.Text)
    hint = db.Column(db.Text)
    correct_answer = db.Column(db.Text)
    completed_message = db.Column(db.Text)
    password = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Post "{self.title}">'