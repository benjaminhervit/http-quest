from flask import Request


def is_browser_request(req: Request) -> bool:
    ua = req.headers.get("User-Agent", "").lower()
    has_browser_headers = {"sec-fetch-site", "sec-fetch-mode", "sec-fetch-dest"} & set(
        h.lower() for h in req.headers.keys()
    )
    if "mozilla" in ua and has_browser_headers:
        return True
    return False
