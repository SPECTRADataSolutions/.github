"""Helper for minting Spectra Assistant GitHub App installation tokens.

This script wraps the JWT + installation-token exchange flow so engineers do not
have to copy inline snippets. Provide the app identifiers and private key via
arguments or environment variables and the script will emit a short-lived token
(suitable for `GITHUB_TOKEN`/`SPECTRA_ASSISTANT_TOKEN`).
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Final

try:  # PyJWT is a tiny dependency and keeps the helper portable across OSes.
    import jwt  # type: ignore
except ModuleNotFoundError as exc:
    raise SystemExit(
        "PyJWT is required. Install via `pip install PyJWT` or `pip install -r scripts/requirements.txt`."
    ) from exc

_DEFAULT_API: Final[str] = os.environ.get("GITHUB_API", "https://api.github.com")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Mint a Spectra Assistant installation token",
    )
    parser.add_argument(
        "--app-id",
        default=os.environ.get("SPECTRA_APP_ID"),
        help="GitHub App ID (env: SPECTRA_APP_ID)",
    )
    parser.add_argument(
        "--installation-id",
        default=os.environ.get("SPECTRA_APP_INSTALLATION_ID"),
        help="Installation ID to target (env: SPECTRA_APP_INSTALLATION_ID)",
    )
    parser.add_argument(
        "--key-file",
        type=Path,
        default=os.environ.get("SPECTRA_APP_PRIVATE_KEY_PATH"),
        help="Path to the Spectra Assistant private key PEM (env: SPECTRA_APP_PRIVATE_KEY_PATH)",
    )
    parser.add_argument(
        "--key",
        default=os.environ.get("SPECTRA_APP_PRIVATE_KEY"),
        help="Raw or base64-encoded private key. Only used when --key-file is absent.",
    )
    parser.add_argument(
        "--ttl",
        type=int,
        default=540,
        help="JWT lifetime in seconds (default: 540 = 9 minutes)",
    )
    parser.add_argument(
        "--api",
        default=_DEFAULT_API,
        help="GitHub API base URL (default: %(default)s)",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json", "token"),
        default="text",
        help="Output format: human text, raw JSON, or bare token",
    )
    return parser.parse_args()


def _load_private_key(key_path: Path | None, inline_key: str | None) -> str:
    if key_path:
        path = key_path.expanduser()
        if not path.exists():
            raise SystemExit(f"Private key file not found: {path}")
        return path.read_text().strip()
    if inline_key:
        candidate = inline_key.strip()
        # Accept base64-encoded values as well as literal PEM text.
        try:
            decoded = base64.b64decode(candidate, validate=True).decode()
            if decoded.startswith("-----BEGIN"):
                return decoded.strip()
        except (ValueError, UnicodeDecodeError):  # Not base64 – fall back to raw string
            pass
        return candidate
    raise SystemExit("Provide --key-file or --key (or set SPECTRA_APP_PRIVATE_KEY[_PATH]).")


def _build_jwt(app_id: str, private_key: str, ttl: int) -> str:
    if ttl <= 0:
        raise SystemExit("TTL must be positive")
    now = int(time.time())
    payload = {
        "iat": now - 60,
        "exp": now + ttl,
        "iss": app_id,
    }
    token = jwt.encode(payload, private_key, algorithm="RS256")
    return token if isinstance(token, str) else token.decode()


def _request_installation_token(api_base: str, installation_id: str, jwt_token: str) -> dict:
    url = f"{api_base.rstrip('/')}/app/installations/{installation_id}/access_tokens"
    request = urllib.request.Request(
        url,
        method="POST",
        data=b"{}",
        headers={
            "Authorization": f"Bearer {jwt_token}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "User-Agent": "spectra-assistant-helper",
        },
    )
    try:
        with urllib.request.urlopen(request) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as err:
        detail = err.read().decode() if err.fp else err.reason
        raise SystemExit(f"GitHub API error {err.code}: {detail}") from err


def _print_result(payload: dict, output_format: str) -> None:
    token = payload.get("token", "")
    expires_at = payload.get("expires_at", "unknown")
    if output_format == "token":
        print(token)
    elif output_format == "json":
        json.dump(payload, sys.stdout, indent=2)
        print()
    else:
        print("Spectra Assistant token minted ✅")
        print(f"Expires at: {expires_at}")
        print()
        print("Export the token in your shell:")
        print(f"  PowerShell : $env:GITHUB_TOKEN = '{token}'")
        print(f"  Bash/zsh   : export GITHUB_TOKEN='{token}'")
        print()
        print("(Token is also available via --format token for scripting.)")


def main() -> None:
    args = _parse_args()
    if not args.app_id:
        raise SystemExit("Missing --app-id (or SPECTRA_APP_ID)")
    if not args.installation_id:
        raise SystemExit("Missing --installation-id (or SPECTRA_APP_INSTALLATION_ID)")
    private_key = _load_private_key(args.key_file, args.key)
    jwt_token = _build_jwt(args.app_id, private_key, args.ttl)
    token_payload = _request_installation_token(args.api, args.installation_id, jwt_token)
    _print_result(token_payload, args.format)


if __name__ == "__main__":  # pragma: no cover
    main()
