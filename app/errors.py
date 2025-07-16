class GameError(Exception):
    def __init__(self, message:str, code:int = 400):
        self.message = message
        self.code = code
        super().__init__(message)
        
class ValidationError(GameError): pass
class AuthenticationError(GameError): pass
class ParsingError(GameError): pass
class QuestError(GameError): pass
# class MethodNotAllowed(Exception) : pass
# class MissingData(Exception) : pass
# class SettingNotFound(Exception) : pass
# class Unauthorized(Exception) : pass
# class InvalidInputLocation(Exception) : pass