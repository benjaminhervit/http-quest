def is_browser_request(req):
    ua = req.headers.get("User-Agent", "").lower()
    has_browser_headers = ({"sec-fetch-site", "sec-fetch-mode", 
                            "sec-fetch-dest"} 
                           & set(h.lower() for h in req.headers.keys()))

    return "mozilla" in ua and has_browser_headers