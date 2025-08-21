from flask import Request
from app.utils import parser_utils
from app.errors import ParsingError, AuthenticationError
from app.enums import StatusCode
from app.models import User


def authenticate_with_username(req: Request) -> str:
    """
    Primary authentication, since the purpose is to learn to send requests,
    not security. The server holds no passwords, personal information, etc.
    """

    username = parser_utils.get_auth_username(req)
    if not username:
        raise ParsingError(
            "Validator received no user."
            "Check if you have made your authorization"
            "header correctly.",
            StatusCode.BAD_REQUEST.value,
        )

    if not User.user_exists(username):
        raise AuthenticationError(
            (
                f"Username {username} not recognized."
                "Check spelling or sign up at"
                "/auth/register"
            ),
            StatusCode.BAD_REQUEST.value,
        )

    return username


def try_authenticate(req: Request) -> str | None:
    """Silent version: returns None on expected auth/parse failures."""
    try:
        return authenticate_with_username(req)
    except (ParsingError, AuthenticationError):
        return None  # silent fail, mostly used for request_snapshot


def no_authentication(*args, **kwargs) -> str:
    """
    Mostly used in the early quests where the player
    has not learned how to authenticate
    """
    return "Unknown Player"
