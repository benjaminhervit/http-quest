
from enum import Enum
#inspired by https://www.w3.org/Protocols/HTTP/HTRESP.html
class LevelEnum(Enum):
    LEADERBOARD = "Leaderboard"
    REGISTRATION = "Registration"
    THE_TEST = "The_Test"
    THE_MONSTER = "The_Monster"
    THE_GATE = "The_Gate"
    THE_THRONE_ROOM = "The_Throne"
    THE_CROWN = "The_Crown"
    SPEAK_TO_JASON = "Jason"
    GAME_OVER = "GAME_OVER"

class Level:
    def __init__(self, name, level_id, description=None, riddle=None, hint=None, correct_answer=None, wrong_answer_response=None, victory_message=None, exp=1, directions=None):
        self.id = level_id
        self.name = name
        self.description = description
        self.quest = riddle
        self.hint = hint
        self.correct_answer = correct_answer
        self.wrong_answer_response = wrong_answer_response
        self.exp = exp
        self.directions = directions
        self.victory_message_template = victory_message
    
    def get_failed_request_info(self):
        return {
            'success':False,
            'directions':self.directions,
        }
    
    def get_welcome_info(self):
        return {
            'success':True,
            'name':self.name,
            'description':self.description,
            'quest':self.quest,
            'hint':self.hint,
        }
    
    def get_wrong_answer_info(self):
        return {
            'success':False,
            'name':self.name,
            'directions':self.directions,
            'description':self.description,
            'quest':self.quest,
            'hint':self.hint,
            'answer_response':self.wrong_answer_response
        }
        
    def get_victory_info(self, party, next_level_directions):
        return {
            'success':True,
            'name':self.name,
            'description':self.description,
            'quest':self.quest,
            'hint':self.hint,
            'answer_response':self.victory_message_template.format(party=party),
            'next_level':next_level_directions
        }
    
    def set_directions(self, directions):
        self.directions = directions
    
    def set_description(self, description):
        self.description = description
        
    def set_hint(self, hint):
        self.hint = hint
        
    def set_correct_answer(self, correct_answer):
        self.correct_answer = correct_answer
        
    def set_wrong_answer_response(self, response):
        self.wrong_answer_response = response
        
    def set_experience(self, newExpValue):
        self.exp = newExpValue
        
    def set_quest(self, riddle):
        self.quest = riddle
        
    def set_victory_message_template(self, message):
        self.victory_message_template = message
    
    def answer_is_correct(self, answer):
        return False
    
class RegisterLevel(Level):
    def __init__(self):
        super().__init__('Register', LevelEnum.REGISTRATION)
        
    def answer_is_correct(self, answer):
        return answer
    
class TestLevel(Level):
    def __init__(self):
        super().__init__('The Test', LevelEnum.THE_TEST)
        
    def answer_is_correct(self, answer):
        if answer:
            try:
                return answer == 42
            except TypeError:
                return False
        return False
    
class GitLevel(Level):
    def __init__(self):
        super().__init__('The Git Monster', LevelEnum.THE_MONSTER)
        
    def answer_is_correct(self, answer):
        if answer:
            try:
                return answer.strip().lower() == "add commit pull push"
            except TypeError:
                return False
        return False
    
class GateLevel(Level):
    def __init__(self):
        super().__init__('The Gate', LevelEnum.THE_GATE)
        
    def answer_is_correct(self, answer):
        if answer:
            try:
                return answer.strip().lower() == "mellon"
            except TypeError:
                return False
        return False
    
class ThroneLevel(Level):
    def __init__(self):
        super().__init__('The Throne', LevelEnum.THE_THRONE_ROOM)
        
    def answer_is_correct(self, answer):
        if answer:
            try:
                return answer == "jason where is the crown?"
            except TypeError:
                return False
        return False
    
class CrownLevel(Level):
    def __init__(self):
        super().__init__('The Crown', LevelEnum.THE_CROWN)
        
    def answer_is_correct(self, answer):
        if answer:
            try:
                return answer == "give me my new cool hat jason"
            except TypeError:
                return False
        return False
    
class JasonLevel(Level):
    def __init__(self):
        super().__init__('Jason', LevelEnum.SPEAK_TO_JASON)
        
    def answer_is_correct(self, answer):
        if answer:
            try:
                answer == "jason where is the crown?"
            except TypeError:
                return False
        return False
    
class GameOverLevel(Level):
    def __init__(self):
        super().__init__('GAME OVER', LevelEnum.GAME_OVER)
        
    def answer_is_correct(self, answer):
        return False