from typing import Any, Dict
from flask import Request, Response, request
from werkzeug.datastructures import FileStorage
import base64
import datetime as dt

MAX_BODY_BYTES = 8 * 1024 # 8kb

# headers to avoid saving
SENSITIVE_HEADERS = {"authorization", "cookie", "set-cookie", "x-api-key"}

TEXTUAL_CT = (
    "application/json",
    "application/xml",
    "application/javascript",
    "text/",
    "application/x-www-form-urlencoded",
)


def _now_iso() -> str:
    return dt.datetime.utcnow().isoformat(timespec="seconds") + "Z"


def _headers_to_safe_dict(headers) -> Dict[str, Any]:
    return {k: v for k, v in headers.items() if k.lower() not in SENSITIVE_HEADERS}

def snapshot_request(req: Request, username: str, include_body=True) -> Dict[str, Any]:
    
    body_str: str | None = None
    ct = (req.mimetype or "").lower()
    is_textual = any(ct.startswith(pfx) for pfx in ("text/",)) or ct in TEXTUAL_CT
    
    if include_body:
        raw = req.get_data(cache=True) or b""
        raw = raw[:MAX_BODY_BYTES]
        if is_textual:
            try:
                body_str = raw.decode(req.charset or "utf-8", errors="replace")
            except Exception:
                body_str = raw.decode("utf-8", errors="replace")

    json_payload = None
    if req.is_json:
        try:
            json_payload = req.get_json(silent=True)
        except Exception:
            json_payload = None
    
    form_data = req.form.to_dict(flat=False) if req.form else None
    
    return {
        "ts": _now_iso(),
        "user": username,
        "remote_addr": req.headers.get("X-Forwarded-For", req.remote_addr) or "Unknown",
        "method": req.method,
        "scheme": req.scheme,
        "host": req.host,
        "path": req.path,
        "full_url": req.url,
        "endpoint": req.endpoint,
        "blueprint": req.blueprint,
        "query": req.args.to_dict(flat=False),
        "headers": _headers_to_safe_dict(req.headers),
        "cookies_present": bool(req.cookies),
        "content_type": req.content_type,
        "content_length": req.content_length,
        "json": json_payload,
        "form": form_data,
        "body_text": body_str
    }

    
def snapshot_response(resp: Response, include_body=True) -> Dict[str, Any]:
    body_text = None

    ct = (resp.mimetype or "").lower()
    is_textual = ct.startswith("text/") or ct in TEXTUAL_CT

    if include_body:
        raw = resp.get_data() or b""
        raw = raw[:MAX_BODY_BYTES]
        if is_textual:
            try:
                body_text = raw.decode(resp.charset or "utf-8", errors="replace")
            except Exception:
                body_text = raw.decode("utf-8", errors="replace")

        return {
            "status": resp.status,
            "status_code": resp.status_code,
            "headers": _headers_to_safe_dict(resp.headers),
            "content_type": resp.content_type,
            "content_length": resp.calculate_content_length(),
            "body_text": body_text,
        }
