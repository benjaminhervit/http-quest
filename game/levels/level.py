
from level_enum import LevelState, LevelEnum
class Level:
    def __init__(self, name, level_id, entry_method, answer_method, next_level:'Level'):
        #basic attributes
        self.id:LevelEnum = level_id
        self.name:str = name
        self.exp:int = 1
        self.entry_method:str = entry_method
        self.answer_method:str = answer_method
        self.state:LevelState = LevelState.INACTIVE
        self.next_level:'Level' = next_level
        self.correct_answer = None
        
        #look up for state and executing the level
        self.map_state_run = {
            LevelState.WELCOME : self.run_welcome,
            LevelState.STARTED : self.run_started,
            LevelState.COMPLETED : self.run_completed,
            LevelState.INACTIVE : self.run_inactive
        }
        
        self.map_state_method = {
            LevelState.WELCOME : [self.entry_method],
            LevelState.STARTED : [self.answer_method],
            LevelState.COMPLETED : [self.answer_method, self.entry_method],
            LevelState.INACTIVE : ['INACTIVE']
        }
        
        #level text
        self.directions = None
        self.description = None
        self.quest = None
        self.hint = None
        self.correct_answer = None
        self.wrong_answer_response = None
        self.victory_message_template = None
        self.method_does_not_match_state = "You need to work on your METHODology."
    
    def run_level(self, **kwargs):
        return self.map_state_run.get(self.state, KeyError ('level state not found...'))(kwargs)
    
    def run_welcome(self, **kwargs):
        method = kwargs.get('method', False)
        if self.method_approved(method):
            self.update_state(LevelState.STARTED)
            return True
        return False
    
    def run_started(self, **kwargs):
        method = kwargs.get('method', '')
        answer = kwargs.get('answer', '')
        
        if self.method_approved(method) and answer and self.answer_is_correct(answer):
            self.update_state(LevelState.COMPLETED)
            return True
        return False
    
    def run_completed(self, **kwargs):
        method = kwargs.get('method', '')
        if self.method_approved(method):
            return True
        return False
    
    def run_inactive(self, **kwargs):
        method = kwargs.get('method', '')
        if self.method_approved(method):
            return True
        return False
    
    def create_level_report(self, **kwargs):
        print(kwargs)
        report = {
            'name': self.name,
            'state': self.state,
            'directions' : self.directions if not self.is_in_state(LevelState.INACTIVE) else 'TBD',
            'description' : self.description if not self.is_in_state(LevelState.INACTIVE) else 'TBD',
            'quest' : self.quest if not self.is_in_state(LevelState.INACTIVE) else 'TBD',
            'hint' : self.hint if not self.is_in_state(LevelState.INACTIVE) else 'TBD',
            'next_level' : self.next_level.name if self.state == LevelState.COMPLETED else 'TBD',
            'correct_answer' : self.correct_answer if self.is_in_state(LevelState.COMPLETED) else 'TBD',
            'victory_message' : self.hint if self.is_in_state(LevelState.COMPLETED) else 'TBD',
        }
        
        
        
        username = kwargs.get('username','')
        answer = kwargs.get('answer','')
        next_level:Level = kwargs.get('next_level', None)
        
        answer_success = self.answer_is_correct(answer)
        level_report = self.get_victory_info(username, next_level) if answer_success else self.get_wrong_answer_info()
        level_report.update({'next_level':next_level.directions if answer_success else "One level at a time..."})
        level_report.update({'success':answer_success})
        return level_report        
    
    def is_in_state(self, state:LevelState):
        return self.state == state
    
    def method_approved(self, incoming_method):
        if incoming_method and incoming_method in self.map_state_method.get(incoming_method, []):
            return True
        return False
        
    def answer_is_correct(self, answer):
        return False
    
    def update_state(self, new_state:LevelState):
        self.state = new_state
    
    #GETTERS
    def get_next_level(self):
        return self.next_level
    
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
    
    #SETTERS
    def set_next_level(self, next_level:'Level'):
        self.next_level = next_level
    
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
    
def exec_level_entry(level:Level, *args):
    return level.get_welcome_info

def exec_level_conclusion(level:Level, next_level:Level, username, answer):
    return level.get_welcome_info(level=level, next_level=next_level, username=username, answer=answer)