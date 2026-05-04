#!/usr/bin/env python3
"""
ONE-TIME SETUP for a Sirion CI managed agent.

Run this once locally per agent. It:
  1. Uploads the seed files via the Files API → persists file_ids
  2. Creates a cloud environment → persists env_id
  3. Creates the agent with the specified system prompt → persists agent_id
  4. Writes everything to .env so run.py (and GitHub Actions) can read them back

To UPDATE the agent later (tweak the system prompt, add a tool), run this script
with `--update`. It will call agents.update() on the existing agent_id, which
bumps the version. Never re-create the agent — versioning is load-bearing.

Usage:
    python setup.py                                    # setup blog curator (default)
    python setup.py --agent youtube                    # setup youtube curator
    python setup.py --agent release-notes              # setup release notes curator
    python setup.py --agent podcast                    # setup podcast curator
    python setup.py --agent pattern                    # setup pattern detector
    python setup.py --update                           # update existing agent
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path

import anthropic
import httpx
from dotenv import dotenv_values, load_dotenv, set_key

# --------------------------------------------------------------------------
# Paths
# --------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
ENV_FILE = PROJECT_ROOT / ".env"

SEED_DIR = PROJECT_ROOT / "seed-templates"

AGENT_CONFIGS = {
    "blog": {
        "prompt_file": "kb-blog-curator.system.md",
        "name": "sirion-blog-curator",
        "description": "Monitors competitor blogs, newsrooms, and substacks for Sirion competitive intelligence.",
        "env_key_prefix": "BLOG",
    },
    "youtube": {
        "prompt_file": "kb-youtube-curator.system.md",
        "name": "sirion-youtube-curator",
        "description": "Monitors competitor YouTube channels for product demos, webinars, and conference talks.",
        "env_key_prefix": "YOUTUBE",
    },
    "release-notes": {
        "prompt_file": "kb-release-notes-curator.system.md",
        "name": "sirion-release-notes-curator",
        "description": "Monitors competitor release notes and changelogs for shipped capabilities.",
        "env_key_prefix": "RELEASE_NOTES",
    },
    "podcast": {
        "prompt_file": "kb-podcast-curator.system.md",
        "name": "sirion-podcast-curator",
        "description": "Monitors industry podcasts for competitor mentions and CLM market trends.",
        "env_key_prefix": "PODCAST",
    },
    "pattern": {
        "prompt_file": "kb-pattern-detector.system.md",
        "name": "sirion-pattern-detector",
        "description": "Weekly cross-signal pattern detection across all Sirion CI sources.",
        "env_key_prefix": "PATTERN",
    },
}

SEED_FILES = [
    ("subscriptions.md",    "text/markdown"),
    ("interests_seed.md",   "text/markdown"),
    ("topic_taxonomy.md",   "text/markdown"),
    ("url_sources.json",    "application/json"),
]

MOUNT_ROOT = "/workspace/seed"
MANAGED_AGENTS_BETA_HEADER = "managed-agents-2026-04-01"
ANTHROPIC_VERSION_HEADER = "2023-06-01"
ANTHROPIC_API_BASE = "https://api.anthropic.com"


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------

def load_env() -> dict[str, str]:
    if not ENV_FILE.exists():
        ENV_FILE.touch()
    return {k: v for k, v in dotenv_values(ENV_FILE).items() if v is not None}


def save_env_key(key: str, value: str) -> None:
    set_key(str(ENV_FILE), key, value, quote_mode="never")


def _managed_agents_request(method: str, path: str, payload: dict) -> dict:
    """Direct API fallback for managed agents endpoints unavailable in older SDKs."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise SystemExit("ANTHROPIC_API_KEY is required.")

    headers = {
        "x-api-key": api_key,
        "anthropic-version": ANTHROPIC_VERSION_HEADER,
        "anthropic-beta": MANAGED_AGENTS_BETA_HEADER,
    }
    url = f"{ANTHROPIC_API_BASE}{path}"
    with httpx.Client(timeout=90) as http:
        response = http.request(method=method, url=url, headers=headers, json=payload)
    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        raise RuntimeError(
            f"Managed Agents API call failed ({method} {path}): "
            f"{exc.response.status_code} {exc.response.text}"
        ) from exc
    return response.json()


def upload_seed_files(client: anthropic.Anthropic) -> dict[str, str]:
    """Upload each seed file; return {filename: file_id}."""
    file_ids: dict[str, str] = {}
    for name, _ in SEED_FILES:
        path = SEED_DIR / name
        if not path.exists():
            raise FileNotFoundError(f"Seed file missing: {path}")
        print(f"  uploading {name} ({path.stat().st_size:,} bytes)...", flush=True)
        with path.open("rb") as f:
            uploaded = client.beta.files.upload(file=f)
        print(f"    → {uploaded.id}")
        file_ids[name] = uploaded.id
    return file_ids


def create_environment(client: anthropic.Anthropic) -> str:
    payload = {
        "name": "kb-blog-curator-env",
        "config": {
            "type": "cloud",
            "networking": {"type": "unrestricted"},
        },
    }
    if hasattr(client.beta, "environments"):
        env = client.beta.environments.create(**payload)
        return env.id
    env = _managed_agents_request("POST", "/v1/environments", payload)
    return env["id"]


def create_agent(client: anthropic.Anthropic, system_prompt: str, name: str, description: str) -> tuple[str, str]:
    payload = {
        "name": name,
        "description": description,
        "model": "claude-sonnet-4-6",
        "system": system_prompt,
        "tools": [
            {
                "type": "agent_toolset_20260401",
                "default_config": {
                    "enabled": True,
                    "permission_policy": {"type": "always_allow"},
                },
            }
        ],
    }
    if hasattr(client.beta, "agents"):
        agent = client.beta.agents.create(**payload)
        return agent.id, str(agent.version)
    agent = _managed_agents_request("POST", "/v1/agents", payload)
    return agent["id"], str(agent["version"])


def update_agent(client: anthropic.Anthropic, agent_id: str, system_prompt: str, current_version: str) -> str:
    """Update the existing agent. Returns the new version string.

    `current_version` is the version we're updating FROM — required by the API
    as an optimistic-concurrency check.
    """
    payload = {
        "version": int(current_version),
        "system": system_prompt,
        "tools": [
            {
                "type": "agent_toolset_20260401",
                "default_config": {
                    "enabled": True,
                    "permission_policy": {"type": "always_allow"},
                },
            }
        ],
    }
    if hasattr(client.beta, "agents"):
        updated = client.beta.agents.update(agent_id, **payload)
        return str(updated.version)
    updated = _managed_agents_request("PATCH", f"/v1/agents/{agent_id}", payload)
    return str(updated["version"])


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agent", choices=list(AGENT_CONFIGS.keys()), default="blog",
                        help="Which agent to set up (default: blog)")
    parser.add_argument("--update", action="store_true",
                        help="Update the existing agent with the current system prompt (bumps version)")
    args = parser.parse_args()

    config = AGENT_CONFIGS[args.agent]
    prompt_file = PROJECT_ROOT / "agents" / config["prompt_file"]
    prefix = config["env_key_prefix"]

    # Support local repo .env and workspace-root .env without requiring manual export.
    load_dotenv(dotenv_path=PROJECT_ROOT.parent / ".env", override=False)
    load_dotenv(dotenv_path=ENV_FILE, override=False)

    if not prompt_file.exists():
        raise SystemExit(f"System prompt not found: {prompt_file}")
    system_prompt = prompt_file.read_text(encoding="utf-8")

    client = anthropic.Anthropic()
    env = load_env()

    if args.update:
        agent_id_key = f"{prefix}_AGENT_ID"
        version_key = f"{prefix}_AGENT_VERSION"
        agent_id = env.get(agent_id_key)
        current_version = env.get(version_key)
        if not agent_id or not current_version:
            raise SystemExit(f"{agent_id_key}/{version_key} not in .env — run without --update first.")
        print(f"Updating agent {agent_id} (from version {current_version})...")
        new_version = update_agent(client, agent_id, system_prompt, current_version)
        save_env_key(version_key, new_version)
        print(f"✓ Agent updated to version {new_version}")
        return

    print("=" * 60)
    print(f"{config['name']} — one-time setup")
    print("=" * 60)

    # 1. Seed files (shared across all agents)
    if "SEED_FILE_IDS" not in env:
        print("\n[1/3] Uploading seed files...")
        file_ids = upload_seed_files(client)
        seed_file_ids_str = ",".join(f"{name}:{fid}" for name, fid in file_ids.items())
        save_env_key("SEED_FILE_IDS", seed_file_ids_str)
    else:
        print("\n[1/3] Seed files already uploaded (SEED_FILE_IDS in .env).")

    # 2. Environment (shared across all agents)
    if "ENV_ID" not in env:
        print("\n[2/3] Creating environment...")
        env_id = create_environment(client)
        save_env_key("ENV_ID", env_id)
        print(f"    → {env_id}")
    else:
        print(f"\n[2/3] Environment already created: {env['ENV_ID']}")

    # 3. Agent (per-agent)
    agent_id_key = f"{prefix}_AGENT_ID"
    version_key = f"{prefix}_AGENT_VERSION"
    if agent_id_key not in env:
        print(f"\n[3/3] Creating agent: {config['name']}...")
        agent_id, version = create_agent(client, system_prompt, config["name"], config["description"])
        save_env_key(agent_id_key, agent_id)
        save_env_key(version_key, version)
        print(f"    → {agent_id} (version {version})")
    else:
        print(f"\n[3/3] Agent already created: {env[agent_id_key]}")

    print("\n" + "=" * 60)
    print("Setup complete. IDs saved to .env:")
    print("=" * 60)
    final_env = load_env()
    for key in ("SEED_FILE_IDS", "ENV_ID", agent_id_key, version_key):
        if key in final_env:
            val = final_env[key]
            display = val if len(val) < 80 else val[:77] + "..."
            print(f"  {key}={display}")

    print(f"\nTo set up the next agent, run: python setup.py --agent <name>")


if __name__ == "__main__":
    main()
