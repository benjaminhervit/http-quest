from app import create_app
from app.extensions import db
from app.models import User, Quest
from app.blueprints.quests.get_all_quests import get_all_quests

def create_and_seed_app(config_class=None):
    
    from app.config import Config  # avoid circular import
    
    app = create_app(config_class or Config)

    with app.app_context():
        db.drop_all()
        db.create_all()
        
        all_quests = get_all_quests()
        for q in all_quests:
            db.session.add(Quest(title=q.title))

        db.session.commit()

        db.session.add(User(username="admin"))
        db.session.commit()

    return app
