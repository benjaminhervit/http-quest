from app.enums import ParserKey, StatusCode
from app.models.quest import Quest
from app.errors import ParsingError

class QuestParser:
    @staticmethod
    def get_settings(quest: Quest):
        try:
            return {
                ParserKey.METHOD_DATA: QuestParser.get_keys_list(
                    quest.allowed_req_methods) if quest.allowed_req_methods
                else [],
                
                ParserKey.QUERY_KEYS: QuestParser.get_keys_list(
                    quest.query_keys) if quest.query_keys
                else [],
                
                ParserKey.AUTH_TYPE: quest.auth_type,
                ParserKey.ANSWER_KEY: quest.answer_key
                
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
        return [q.strip() for q in string.split(',')]