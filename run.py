# run.py or manage.py
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.quest import Quest
#from app.game.quests_factory import make_all_quests
# from game.quests_factory.make_accept_q import accept_Q
# from game.quests_factory.make_welcome_q import welcome_Q

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()
    
    # create quests
    #all_quests = make_all_quests()
    #db.session.add_all(all_quests)
    # db.session.flush()
    
    # #add dependencies
    # for i in range(1, len(all_quests)):
    #     all_quests[i].prev_quest_id = all_quests[i - 1].id
    # db.session.commit()

    db.session.add(User(username="admin"))
    db.session.commit()

    print("✔️ Database initialized with sample quests.")