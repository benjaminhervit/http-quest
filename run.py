# run.py or manage.py
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.quest import Quest
from app.game.quests import quests
from app.game.quests.accept import accept_Q
from app.game.quests.welcome import welcome_Q

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    db.session.add_all(quests)
    accept_Q.prev_quest_id = welcome_Q.id
    db.session.commit()

    db.session.add(User(username="admin"))
    db.session.commit()

    print("✔️ Database initialized with sample quests.")