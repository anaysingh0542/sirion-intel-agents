#!/usr/bin/env python3
"""
Set up ALL Sirion CI managed agents in one pass.

Creates shared seed files + environment, then creates each of the 5 agents
(blog, youtube, release-notes, podcast, pattern). Writes all IDs to .env
and updates admin.json in the KB repo with the agent/environment IDs.

Usage:
    python setup_all.py
    python setup_all.py --update   # update all agents with current prompts
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPTS_DIR.parent
KB_ADMIN_JSON = PROJECT_ROOT.parent / "sirion-intel-kb" / "_system" / "config" / "admin.json"

AGENT_ORDER = ["blog", "youtube", "release-notes", "podcast", "pattern"]

SOURCE_KEY_MAP = {
    "blog": "blogs",
    "youtube": "youtube",
    "release-notes": "release_notes",
    "podcast": "podcasts",
    "pattern": "pattern_agent",
}

ENV_PREFIX_MAP = {
    "blog": "BLOG",
    "youtube": "YOUTUBE",
    "release-notes": "RELEASE_NOTES",
    "podcast": "PODCAST",
    "pattern": "PATTERN",
}


def run_setup(agent: str, update: bool = False) -> int:
    cmd = [sys.executable, str(SCRIPTS_DIR / "setup.py"), "--agent", agent]
    if update:
        cmd.append("--update")
    print(f"\n{'='*60}")
    print(f"  Setting up: {agent}")
    print(f"{'='*60}\n")
    result = subprocess.run(cmd, cwd=str(PROJECT_ROOT))
    return result.returncode


def update_admin_json() -> None:
    """Read agent IDs from .env and write them into admin.json."""
    if not KB_ADMIN_JSON.exists():
        print(f"\n⚠ admin.json not found at {KB_ADMIN_JSON} — skipping update")
        return

    from dotenv import dotenv_values
    env_file = PROJECT_ROOT / ".env"
    env = {k: v for k, v in dotenv_values(str(env_file)).items() if v is not None}

    admin = json.loads(KB_ADMIN_JSON.read_text(encoding="utf-8"))
    env_id = env.get("ENV_ID")

    for agent_key, source_key in SOURCE_KEY_MAP.items():
        prefix = ENV_PREFIX_MAP[agent_key]
        agent_id = env.get(f"{prefix}_AGENT_ID")
        if source_key in admin.get("sources", {}):
            if agent_id:
                admin["sources"][source_key]["agent_id"] = agent_id
            if env_id:
                admin["sources"][source_key]["environment_id"] = env_id

    KB_ADMIN_JSON.write_text(json.dumps(admin, indent=2) + "\n", encoding="utf-8")
    print(f"\n✓ Updated {KB_ADMIN_JSON} with agent IDs and environment ID")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--update", action="store_true",
                        help="Update all existing agents with current system prompts")
    args = parser.parse_args()

    failures = []
    for agent in AGENT_ORDER:
        rc = run_setup(agent, update=args.update)
        if rc != 0:
            failures.append(agent)
            print(f"\n✗ {agent} failed (exit code {rc})")

    if not args.update:
        update_admin_json()

    print(f"\n{'='*60}")
    if failures:
        print(f"Completed with errors. Failed agents: {', '.join(failures)}")
        print("Fix the issues and re-run setup_all.py (it's idempotent).")
    else:
        print("All agents set up successfully.")
    print(f"{'='*60}")

    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
