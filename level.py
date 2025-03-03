
from enum import Enum
#inspired by https://www.w3.org/Protocols/HTTP/HTRESP.html
class LevelE(Enum):
    HOME = 0
    REGISTER = 1
    THE_TEST = 2
    THE_GIT_MONSTER = 3
    THE_GATE = 4
    THE_THRONE_ROOM = 5
    THE_CROWN = 6

class Level:
    def __init__(self, name, description=None, riddle=None, hint=None, correct_answer=None, wrong_answer_response=None, victory_message=None, exp=1, directions=None):
        self.name = name
        self.description = description
        self.riddle = riddle
        self.hint = hint
        self.correct_answer = correct_answer
        self.wrong_answer_response = wrong_answer_response
        self.exp = exp
        self.directions = directions
        self.victory_message_template = victory_message
    
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
        
    def set_riddle(self, riddle):
        self.riddle = riddle
        
    def set_victory_message_template(self, message):
        self.victory_message_template = message

    def response_get(self, request):
        return self.description + self.hint if self.description and self.hint else ""
    
    def response_post(self, request):
        return "response_post not implemented"
    
    def response_put(self, request):
        return "response_put not implemented"
    
    def response_delete(self, request):
        return "response_delete not implemented"
    
    def answer_is_correct(self, answer):
        return False
    
class RegisterLevel(Level):
    def __init__(self):
        super().__init__('Register')
        
    def answer_is_correct(self, answer):
        return answer
    
class TestLevel(Level):
    def __init__(self):
        super().__init__('The Test')
        
    def answer_is_correct(self, answer):
        if answer:
            try:
                return answer == 42
            except TypeError:
                return False
        return False
    
class GitLevel(Level):
    def __init__(self):
        super().__init__('The Git Monster')
        
    def answer_is_correct(self, answer):
        if answer:
            try:
                return answer.strip().lower() == "add commit pull push"
            except TypeError:
                return False
        return False
    
class GateLevel(Level):
    def __init__(self):
        super().__init__('The Gate')
        
    def answer_is_correct(self, answer):
        if answer:
            try:
                return answer.strip().lower() == "mellon"
            except TypeError:
                return False
        return False
    
class ThroneLevel(Level):
    def __init__(self):
        super().__init__('The Throne')
        
    def answer_is_correct(self, answer):
        if answer:
            try:
                the_ultimate_answer = "Answer to the Ultimate Question of Life, The Universe, and Everything".lower() in answer
                what_is_the_meaning = "what is the meaning with all of this".lower() in answer
                return the_ultimate_answer or what_is_the_meaning
            except TypeError:
                return False
        return False
    
class CrownLevel(Level):
    def __init__(self):
        super().__init__('The Throne')
        
    def answer_is_correct(self, answer):
        if answer:
            try:
                the_ultimate_answer = "Answer to the Ultimate Question of Life, The Universe, and Everything".lower() in answer
                what_is_the_meaning = "what is the meaning with all of this".lower() in answer
                return the_ultimate_answer or what_is_the_meaning
            except TypeError:
                return False
        return False