#!/usr/bin/env python3
"""Print the fully rendered Realtime system prompt.

This is a local prompt-as-code helper: it does not call OpenAI or Twilio. It
imports the app config, so Supabase dynamic settings may load when enabled in
the environment. It then applies optional preview overrides, rebuilds
Config.SYSTEM_MESSAGE, and writes the final prompt to stdout.
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _load_environment() -> None:
    """Load .env before importing config, but do not require a real API key."""
    load_dotenv(PROJECT_ROOT / ".env")
    os.environ.setdefault("OPENAI_API_KEY", "prompt-preview")
    sys.path.insert(0, str(PROJECT_ROOT))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render and print Config.SYSTEM_MESSAGE for prompt review."
    )
    parser.add_argument("--prompt-path", help="Prompt markdown path, default from SYSTEM_INSTRUCTIONS_PATH.")
    parser.add_argument("--company-name", help="Preview COMPANY_NAME.")
    parser.add_argument("--agent-name", help="Preview AGENT_NAME.")
    parser.add_argument("--tone", help="Preview ASSISTANT_TONE.")
    parser.add_argument("--warmth", help="Preview ASSISTANT_WARMTH: neutral, warm, very_warm.")
    parser.add_argument("--expressiveness", help="Preview ASSISTANT_EXPRESSIVENESS: reserved, balanced, expressive.")
    parser.add_argument("--pacing", help="Preview ASSISTANT_PACING: relaxed, moderate, brisk.")
    parser.add_argument("--language", help="Preview ASSISTANT_LANGUAGE.")
    parser.add_argument("--language-switch-policy", help="Preview LANGUAGE_SWITCH_POLICY.")
    parser.add_argument("--accent", help="Preview ASSISTANT_ACCENT.")
    parser.add_argument("--accent-strength", help="Preview ASSISTANT_ACCENT_STRENGTH.")
    parser.add_argument("--model", help="Preview OPENAI_REALTIME_MODEL.")
    parser.add_argument("--reasoning-effort", help="Preview REALTIME_REASONING_EFFORT.")
    args = parser.parse_args()

    _load_environment()

    from config import Config, rebuild_system_message

    if args.prompt_path:
        Config.SYSTEM_INSTRUCTIONS_PATH = args.prompt_path
    if args.company_name:
        Config.COMPANY_NAME = args.company_name
    if args.agent_name is not None:
        Config.AGENT_NAME = args.agent_name
    if args.tone:
        Config.ASSISTANT_TONE = args.tone
    if args.warmth:
        Config.ASSISTANT_WARMTH = args.warmth
    if args.expressiveness:
        Config.ASSISTANT_EXPRESSIVENESS = args.expressiveness
    if args.pacing:
        Config.ASSISTANT_PACING = args.pacing
    if args.language:
        Config.ASSISTANT_LANGUAGE = args.language
    if args.language_switch_policy:
        Config.LANGUAGE_SWITCH_POLICY = args.language_switch_policy
    if args.accent:
        Config.ASSISTANT_ACCENT = args.accent
    if args.accent_strength:
        Config.ASSISTANT_ACCENT_STRENGTH = args.accent_strength
    if args.model:
        Config.OPENAI_REALTIME_MODEL = args.model
    if args.reasoning_effort:
        Config.REALTIME_REASONING_EFFORT = args.reasoning_effort

    rebuild_system_message()
    sys.stdout.write(Config.SYSTEM_MESSAGE)
    if not Config.SYSTEM_MESSAGE.endswith("\n"):
        sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
