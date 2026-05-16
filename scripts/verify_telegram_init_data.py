#!/usr/bin/env python3
"""Verify Telegram WebApp initData for Step3D Mini App backend.

The script has no network calls and does not print tokens. In production the bot token
must come from STEP3D_TELEGRAM_BOT_TOKEN or a secret manager.
"""
from __future__ import annotations

import argparse
import hashlib
import hmac
import os
import time
from dataclasses import dataclass
from urllib.parse import parse_qsl, quote, urlencode


@dataclass(frozen=True)
class VerificationResult:
    ok: bool
    reason: str
    user_id: str | None = None
    auth_date: int | None = None


def _data_check_string(init_data: str) -> tuple[str, str | None, dict[str, str]]:
    pairs = parse_qsl(init_data, keep_blank_values=True, strict_parsing=False)
    values: dict[str, str] = {}
    received_hash: str | None = None
    for key, value in pairs:
        if key == "hash":
            received_hash = value
        else:
            values[key] = value
    check = "\n".join(f"{key}={values[key]}" for key in sorted(values))
    return check, received_hash, values


def make_init_data(fields: dict[str, str], bot_token: str) -> str:
    """Build signed initData for tests/dev fixtures."""
    data_check = "\n".join(f"{key}={fields[key]}" for key in sorted(fields))
    secret_key = hmac.new(b"WebAppData", bot_token.encode(), hashlib.sha256).digest()
    digest = hmac.new(secret_key, data_check.encode(), hashlib.sha256).hexdigest()
    return urlencode({**fields, "hash": digest}, quote_via=quote)


def verify_init_data(init_data: str, bot_token: str, *, max_age_seconds: int = 86400, now: int | None = None) -> VerificationResult:
    if not init_data:
        return VerificationResult(False, "empty initData")
    if not bot_token:
        return VerificationResult(False, "missing bot token")

    data_check, received_hash, values = _data_check_string(init_data)
    if not received_hash:
        return VerificationResult(False, "hash missing")

    secret_key = hmac.new(b"WebAppData", bot_token.encode(), hashlib.sha256).digest()
    expected_hash = hmac.new(secret_key, data_check.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected_hash, received_hash):
        return VerificationResult(False, "hash mismatch")

    raw_auth_date = values.get("auth_date")
    try:
        auth_date = int(raw_auth_date or "0")
    except ValueError:
        return VerificationResult(False, "invalid auth_date")

    now_ts = int(now if now is not None else time.time())
    if max_age_seconds > 0 and (auth_date <= 0 or now_ts - auth_date > max_age_seconds):
        return VerificationResult(False, "initData expired", auth_date=auth_date)
    if auth_date - now_ts > 60:
        return VerificationResult(False, "auth_date is in the future", auth_date=auth_date)

    return VerificationResult(True, "ok", user_id=values.get("user", ""), auth_date=auth_date)


def self_test() -> None:
    token = "123456:TEST_TOKEN"
    now = 1_700_000_000
    fields = {
        "query_id": "AAHdF6IQAAAAAN0XohDhrOrc",
        "user": '{"id":7260915527,"first_name":"Nikita","username":"step_3d_mngr","language_code":"ru"}',
        "auth_date": str(now),
    }
    signed = make_init_data(fields, token)
    ok = verify_init_data(signed, token, now=now)
    assert ok.ok, ok
    tampered = signed.replace("Nikita", "Evil")
    bad = verify_init_data(tampered, token, now=now)
    assert not bad.ok and bad.reason == "hash mismatch", bad
    expired = verify_init_data(signed, token, now=now + 90_000)
    assert not expired.ok and expired.reason == "initData expired", expired
    print("TELEGRAM_INIT_DATA_SELF_TEST_OK")


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify Telegram WebApp initData for Step3D backend.")
    parser.add_argument("--init-data", default="", help="Raw Telegram WebApp initData string")
    parser.add_argument("--token-env", default="STEP3D_TELEGRAM_BOT_TOKEN", help="Environment variable with bot token")
    parser.add_argument("--max-age", type=int, default=86400, help="Max initData age in seconds; 0 disables age check")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        return 0

    result = verify_init_data(args.init_data, os.environ.get(args.token_env, ""), max_age_seconds=args.max_age)
    if result.ok:
        print("TELEGRAM_INIT_DATA_OK")
        return 0
    print(f"TELEGRAM_INIT_DATA_INVALID: {result.reason}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
