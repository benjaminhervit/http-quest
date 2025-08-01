from app.enums import ParserKey, QuestKey, StatusCode
from app.models.quest import Quest
from app.errors import ParsingError

from app.utils import get_clean_list_from_string

class QuestParser:
    @staticmethod
    def get_settings(quest: Quest):
        try:
            return {
                QuestKey.METHOD_DATA: QuestParser.get_keys_list(
                    quest.allowed_req_methods) if quest.allowed_req_methods
                else [],
                
                QuestKey.QUERY_KEYS: QuestParser.get_keys_list(
                    quest.query_keys) if quest.query_keys
                else [],
                
                QuestKey.FORM_KEYS: QuestParser.get_keys_list(
                    quest.form_keys) if quest.form_keys
                else [],
                
                QuestKey.AUTH_TYPE: quest.auth_type,
                QuestKey.ANSWER_KEY: quest.solution_key,
                QuestKey.ANSWER_LOC: quest.solution_location
                
                # TODO: UNCOMMENT PARSERS WHEN RELEVANT FOR NEW QUESTS
                # ParserKey.JSON_KEYS: Parser.get_keys_list(
                #     quest.json_keys) if quest.json_keys
                # else [],
                
                # ParserKey.FORM_KEYS: Parser.get_keys_list(
                #     quest.form_keys) if quest.form_keys
                # else [],
                
                # ParserKey.HEADERS_KEYS: Parser.get_keys_list(
                #     quest.headers_keys) if quest.headers_keys
                # else [],
                
                # ParserKey.USERNAME_LOC: quest.username_loc,
                # ParserKey.TOKEN_LOC: quest.token_loc,
                
            }
        except ParsingError as exc:
            raise ParsingError(f'Failed to parse quest settings: {quest}',
                               code=StatusCode.SERVER_ERROR.value) from exc
            
    @staticmethod
    def get_keys_list(string: str):
        # Helper method to extract keys from string field in Model.
        # E.g: query_keys="a,b,c"
        return get_clean_list_from_string(string, ",")