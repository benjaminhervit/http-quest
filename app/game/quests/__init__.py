from app.game.quests.welcome_quest import welcome_q

quests = [welcome_q]

for q in quests:
    json_q = q.to_json()
    print(json_q)