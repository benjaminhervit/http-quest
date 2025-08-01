from app import create_app
from app.extensions import db
from app.models.user import User
from app.game.quests_factory import make_all_quests

def create_and_seed_app(config_class=None):
    
    from app.config import Config  # avoid circular import
    
    app = create_app(config_class or Config)

    with app.app_context():
        db.drop_all()
        db.create_all()
        
        all_quests = make_all_quests()
        db.session.add_all(all_quests)
        
        for i in range(1, len(all_quests)):
            all_quests[i].prev_quest_id = all_quests[i - 1].id
        db.session.commit()

        db.session.add(User(username="admin"))
        db.session.commit()

    return app
