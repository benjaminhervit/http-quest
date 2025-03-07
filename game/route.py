from game.level import Level

class Route:
    def __init__(self, route, level:Level, next_level:Level, method_func:callable, param_func:callable):
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