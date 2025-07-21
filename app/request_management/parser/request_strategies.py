
from flask import Request
from app.enums import StatusCode, ParserKey, ReqMethodType
from app.errors import ParsingError

# NONE STRAT


def get_none(*args, **kwargs):
    return None

# GET DATA STRATEGIES


def get_json(req: Request) -> dict | None:
    """
    Force and silent to return None output even
    if content-type or json is missing/incorrect
    """
    data = req.get_json(force=True, silent=True)
    if not data or data is None:
        return None
    return data


def get_method(req: Request) -> str:
    m = req.method
    if m not in ReqMethodType:
        raise ParsingError(f'Request method ({m}) is not accepted.',
                           code=StatusCode.BAD_REQUEST)
    return req.method


def get_query(req: Request) -> dict | None:
    return req.args.to_dict() if req.args else None


def get_form(req: Request) -> dict | None:
    if get_method(req) == ReqMethodType.GET:
        return None
    return req.form.to_dict() if req.form else None

    
def get_headers(req: Request):
    #  not conventional dict but has same look up functionality
    #  doc: https://werkzeug.palletsprojects.com/en/stable/datastructures/#werkzeug.datastructures.Headers
    return req.headers


def get_path(req: Request) -> list[str] | None:
    print(f"REQ PATH: {req.path}")
    path = req.path.split('/')
    return [p.strip() for p in path if p.strip()]

# USERNAME STRATEGIES


def get_username(data: dict):
    #by convention username is always with key 'username'
    return data.get(ParserKey.USERNAME.value)


def get_username_from_query(req: Request):
    data: dict | None = get_query(req)
    return get_username(data) if data else None


def get_username_from_form(req: Request):
    data: dict | None = get_form(req)
    return get_username(data) if data else None


def get_username_from_json(req: Request):
    data: dict | None = get_json(req)
    return get_username(data) if data else None

# TOKEN STRATEGIES
#TODO: Will implement when token is introduced