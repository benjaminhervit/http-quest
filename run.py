# run.py or manage.py
from app import create_app
from app.extensions import db
from app.models import User, Quest
from app.blueprints.quests.get_all_quests import get_all_quests

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    all_quests = get_all_quests()
    for q in all_quests:
        db.session.add(Quest(title=q.title))
    db.session.commit()

    admin_exists = User.get_by_username("admin")
    if not admin_exists:
        db.session.add(User(username="admin"))
        db.session.commit()

    print("✔️ Database initialized with sample quests.")
