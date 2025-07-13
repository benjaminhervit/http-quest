from app.game.enums.game_state import GameState
class Quest:
    def __init__(self):
        #QUEST SPECIFIC
        self.title = "Welcome"
        self.directions = "Get here by going to game/level/welcome"
        
        #
        self.welcome_text = "Welcome to a CRUDe game!"
        self.description = "You stand in front of an epic quest with nothing but your hard earned knowledge from a lecture you never attended."
        self.quest = "Write your name in the PATH to glory"
        self.answer = "Test"
        
        #responses
        self.response_wrong = "Absolutely not correct - not even one bit. I mean... holy..!"
        self.response_correct = "What a genius you are! This is out standing! The world will soon be safe again!"
        self.response_completed = "why are you still here???"
        
        #next level/quest
        self.next_quest_directions = "there should be some/path/descriptions/here"
    
    def __repr__(self):
        return f'<Post "{self.title}">'