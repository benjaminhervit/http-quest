from flask import Request
from typing import Callable

from app.utils import send_response

from app.enums import StatusCode
from app.errors import ParsingError, ValidationError, GameError, AuthenticationError
from app.utils import content_generator
from app.quest import QuestData


class QuestRequestHandler:
    @classmethod
    def validate_handlers_map(cls, handlers_map: dict, valid_methods: list) -> bool:
        for m in valid_methods:
            if m not in handlers_map:
                raise ValueError(f"Missing handler for method {m}")
        return True

    @classmethod
    def execute(
        cls,
        req: Request,
        quest: QuestData,
        authenticator: Callable,
        handlers_map: dict,
        # valid_req_methods: list,
        html_template: str = "quest_renderer.html",
    ):
        # SKIPPING INTERNAL METHOD-REQ CHECK.
        # TODO: Move this check into a test file for each quest. 
        # cls.validate_handlers_map(handlers_map, valid_req_methods)
        if not isinstance(authenticator, Callable):
            raise ValueError("Passed authenticator is not callable")

        try:
            #  Authenticate user
            username = authenticator(req=req)
            if not username:
                raise AuthenticationError(
                    "Could not authenticate user", StatusCode.UNAUTHORIZED.value
                )

            #  Setup quest
            handler = handlers_map.get(req.method)
            if not handler:
                raise GameError(
                    f"Method {req.method} is not allowed for this quest. Read the quest again.",
                    StatusCode.BAD_REQUEST.value,
                )

            content = handler(quest=quest, req=req)

            return send_response(req, content, StatusCode.OK.value, html_template)

        # error handling
        except ParsingError as e:
            content = content_generator.create_error_msg(str(e), "ParsingError", e.code)
            return send_response(
                req, content, StatusCode.SERVER_ERROR.value, html="error_message.html"
            )

        except ValidationError as e:
            content = content_generator.create_error_msg(
                str(e), "ValidationError", e.code
            )
            return send_response(req, content, e.code, html="error_message.html")

        except GameError as e:
            content = content_generator.create_error_msg(str(e), "GameError", e.code)
            return send_response(req, content, e.code, html="error_message.html")

        except ValueError as e:
            content = content_generator.create_error_msg(
                str(e), "ValueError", StatusCode.BAD_REQUEST.value
            )
            return send_response(
                req, content, StatusCode.BAD_REQUEST.value, html="error_message.html"
            )

        except TypeError as e:
            content = content_generator.create_error_msg(
                str(e), "TypeError", StatusCode.BAD_REQUEST.value
            )
            return send_response(
                req, content, StatusCode.BAD_REQUEST.value, html="error_message.html"
            )
