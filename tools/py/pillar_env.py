"""Pillar pages env + auth helper.

Provides:
- ALLOWED_POST_IDS: frozenset of the 15 pillar post IDs we are allowed to touch.
- PILLAR_OF: mapping post_id -> pillar number (1..5).
- assert_allowed(post_id): exit hard if a script tries to touch a non-pillar post.
- make_session(): authenticated requests.Session against suriota.com with
  X-WP-Nonce header pre-set, matching the working pattern used elsewhere
  in this repo (see tools/py/apply_zh_translations.py).
- Module constants: WP_BASE, WP_USER, WP_PASS, ROOT.

Loads .env from the repo root manually (no external deps required).
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import requests

# Repo root = two levels up from this file (tools/py/pillar_env.py -> repo root).
ROOT = Path(__file__).resolve().parents[2]


def _load_dotenv(path: Path) -> None:
    """Minimal .env loader. Ignores comments and blank lines. No external deps."""
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        # Don't overwrite an explicitly-set environment variable.
        os.environ.setdefault(key, value)


_load_dotenv(ROOT / ".env")

WP_BASE: str = os.environ.get("WP_BASE", "https://suriota.com").rstrip("/")
WP_USER: str = os.environ.get("WP_USER", "")
WP_PASS: str = os.environ.get("WP_PASS", "")

# --- Scope lock: the 15 pillar posts. NEVER touch anything outside this set. ---
ALLOWED_POST_IDS: frozenset[int] = frozenset(
    {
        # Pillar 1
        5554, 5555, 5556,
        # Pillar 2
        5557, 5558, 5566,
        # Pillar 3
        5567, 5568, 5569,
        # Pillar 4
        5570, 5571, 5572,
        # Pillar 5
        5573, 5574, 5575,
    }
)

PILLAR_OF: dict[int, int] = {
    5554: 1, 5555: 1, 5556: 1,
    5557: 2, 5558: 2, 5566: 2,
    5567: 3, 5568: 3, 5569: 3,
    5570: 4, 5571: 4, 5572: 4,
    5573: 5, 5574: 5, 5575: 5,
}


def assert_allowed(post_id: int) -> None:
    """Hard-stop if post_id is not in the pillar allowlist.

    This is the scope lock for all pillar scripts. Calling it ensures we
    cannot accidentally mutate sitewide pages, the homepage, snippets, etc.
    """
    if int(post_id) not in ALLOWED_POST_IDS:
        allowed = ", ".join(str(p) for p in sorted(ALLOWED_POST_IDS))
        sys.exit(
            f"REFUSED: post_id={post_id} is not in the pillar allowlist. "
            f"Allowed IDs: {allowed}"
        )


def make_session() -> requests.Session:
    """Return an authenticated requests.Session with X-WP-Nonce pre-set.

    Uses the wp-login.php form + admin-ajax rest-nonce pattern that is
    already proven in this repo (see tools/py/apply_zh_translations.py).
    """
    if not WP_USER or not WP_PASS:
        sys.exit(
            "REFUSED: WP_USER / WP_PASS not set. "
            "Create a .env file in the repo root (see .env.example)."
        )

    session = requests.Session()

    login = session.post(
        f"{WP_BASE}/wp-login.php",
        data={
            "log": WP_USER,
            "pwd": WP_PASS,
            "wp-submit": "Log In",
            "redirect_to": f"{WP_BASE}/wp-admin",
            "testcookie": "1",
        },
        timeout=30,
        allow_redirects=True,
    )
    # wp-login redirects on success; either way we now need the rest-nonce.
    if login.status_code >= 500:
        sys.exit(f"REFUSED: wp-login.php returned HTTP {login.status_code}")

    nonce_resp = session.get(
        f"{WP_BASE}/wp-admin/admin-ajax.php?action=rest-nonce", timeout=30
    )
    nonce = nonce_resp.text.strip()
    if not nonce or len(nonce) > 64:
        sys.exit(
            f"REFUSED: could not fetch a valid rest-nonce "
            f"(status={nonce_resp.status_code}, len={len(nonce)})"
        )

    session.headers.update(
        {
            "X-WP-Nonce": nonce,
            "Content-Type": "application/json",
        }
    )
    return session


__all__ = [
    "ROOT",
    "WP_BASE",
    "WP_USER",
    "WP_PASS",
    "ALLOWED_POST_IDS",
    "PILLAR_OF",
    "assert_allowed",
    "make_session",
]
