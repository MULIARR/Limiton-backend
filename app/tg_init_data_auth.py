import time
import hmac
import hashlib
import urllib.parse
from fastapi import Request, HTTPException

from config import config


def validate_init_data(init_data_raw: str, bot_token: str, expires_in: int = 3600) -> dict:
    """
    Validates the original data received from the Telegram Mini application.
    Returns a dictionary with the data if the check is successful, otherwise raises ValueError.
    """
    parsed = urllib.parse.parse_qs(init_data_raw, keep_blank_values=True)
    data = {k: v[0] for k, v in parsed.items()}

    if 'hash' not in data:
        raise ValueError("Missing 'hash' in init data")

    received_hash = data.pop('hash')

    sorted_params = sorted(data.items(), key=lambda x: x[0])
    data_check_string = "\n".join(f"{k}={v}" for k, v in sorted_params)

    secret_key = hmac.new(b"WebAppData", bot_token.encode('utf-8'), hashlib.sha256).digest()

    check_hash = hmac.new(secret_key, data_check_string.encode('utf-8'), hashlib.sha256).hexdigest()

    if check_hash != received_hash:
        raise ValueError("Invalid init data: hash mismatch")

    if 'auth_date' not in data:
        raise ValueError("Missing 'auth_date' in init data")
    auth_date = int(data['auth_date'])
    now = int(time.time())
    if now - auth_date > expires_in:
        raise ValueError("Init data expired")

    return data


def get_init_data_from_request(request: Request):
    auth_header = request.headers.get("authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    parts = auth_header.split(" ", 1)
    if len(parts) != 2:
        raise HTTPException(status_code=401, detail="Invalid Authorization header format")

    auth_type, init_data_raw = parts
    if auth_type != "tma":
        raise HTTPException(status_code=401, detail="Unsupported auth type")

    try:
        data = validate_init_data(init_data_raw, config.tg_bot.token, expires_in=3600)
        return data
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
