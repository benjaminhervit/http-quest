
from enum import Enum
#inspired by https://www.w3.org/Protocols/HTTP/HTRESP.html
class LevelEnum(Enum):
    LEADERBOARD = "leaderboard"
    REGISTRATION = "registration"
    THE_TEST = "the_test"
    THE_MONSTER = "the_monster"
    THE_GATE = "the_gate"
    THE_THRONE_ROOM = "the_throne"
    THE_CROWN = "the_crown"
    SPEAK_TO_JASON = "hason"
    GAME_OVER = "game_over"

class Level:
    def __init__(self, name, level_id, secret_key_parser = None, req_data_parser=None, description=None, riddle=None, hint=None, correct_answer=None, wrong_answer_response=None, victory_message=None, exp=1, directions=None):
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
        self.secret_key_parser :callable = secret_key_parser
        self.req_data_parser : callable = req_data_parser
    
    def parse_request_data(self, req):
        return self.req_data_parser(req)

    def parse_secret_key(self, req):
        return self.secret_key_parser(req)
    
    def get_failed_request_info(self):
        return {
            'success':False,
            'directions':self.directions,
        }
    
    def get_welcome_info(self, **kwargs):
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
            'answer_accepted':True,
            'name':self.name,
            'answer_response':self.victory_message_template.format(party=party),
            'next_level':next_level_directions
        }
        
    def set_req_data_parser(self, parser):
        self.req_data_parser = parser
        
    def set_secret_key_parser(self, parser):
        self.secret_key_parser = parser
    
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
    
    def level_report(self, **kwargs):
        print(kwargs)
        username = kwargs.get('username','')
        answer = kwargs.get('answer','')
        next_level:Level = kwargs.get('next_level', None)
        
        answer_success = self.answer_is_correct(answer)
        level_report = self.get_victory_info(username, next_level) if answer_success else self.get_wrong_answer_info()
        level_report.update({'next_level':next_level.directions if answer_success else "One level at a time..."})
        level_report.update({'success':answer_success})
        return level_report
    
class RegisterLevel(Level):
    def __init__(self):
        super().__init__(LevelEnum.REGISTRATION.value, LevelEnum.REGISTRATION)
        
    def answer_is_correct(self, answer):
        return answer
    
class TestLevel(Level):
    def __init__(self):
        super().__init__(LevelEnum.THE_TEST.value, LevelEnum.THE_TEST)
        
    def answer_is_correct(self, answer):
        try:
            answer = int(answer)
            success = answer == 42
            return success
        except TypeError:
            return False
    
class GitLevel(Level):
    def __init__(self):
        super().__init__(LevelEnum.THE_MONSTER.value, LevelEnum.THE_MONSTER)
        
    def answer_is_correct(self, answer):
        if answer:
            try:
                return answer.strip().lower() == "pull/add/commit/push"
            except TypeError:
                return False
        return False
    
class GateLevel(Level):
    def __init__(self):
        super().__init__(LevelEnum.THE_GATE.value, LevelEnum.THE_GATE)
        
    def answer_is_correct(self, answer):
        if answer:
            try:
                return answer.strip().lower() == "mellon"
            except TypeError:
                return False
        return False
    
class ThroneLevel(Level):
    def __init__(self):
        super().__init__(LevelEnum.THE_THRONE_ROOM.value, LevelEnum.THE_THRONE_ROOM)
        
    def answer_is_correct(self, answer):
        if answer:
            try:
                return answer == "jason where is the crown"
            except TypeError:
                return False
        return False
    
class CrownLevel(Level):
    def __init__(self):
        super().__init__(LevelEnum.THE_CROWN.value, LevelEnum.THE_CROWN)
        
    def answer_is_correct(self, answer):
        if answer:
            try:
                return answer == "give me my new cool hat jason"
            except TypeError:
                return False
        return False
    
class JasonLevel(Level):
    def __init__(self):
        super().__init__(LevelEnum.SPEAK_TO_JASON.value, LevelEnum.SPEAK_TO_JASON)
        
    def answer_is_correct(self, answer):
        if answer:
            try:
                answer == "jason where is the crown"
            except TypeError:
                return False
        return False
    
class GameOverLevel(Level):
    def __init__(self):
        super().__init__(LevelEnum.GAME_OVER.value, LevelEnum.GAME_OVER)
        
    def answer_is_correct(self, answer):
        return False

def exec_level_entry(level:Level, *args):
    return level.get_welcome_info

def exec_level_conclusion(level:Level, next_level:Level, username, answer):
    return level.get_welcome_info(level=level, next_level=next_level, username=username, answer=answer)