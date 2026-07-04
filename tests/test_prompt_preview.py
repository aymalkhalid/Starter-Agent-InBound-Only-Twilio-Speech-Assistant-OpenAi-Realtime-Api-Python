"""Tests for prompt-as-code preview helper."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_prompt_preview_script_prints_rendered_system_prompt():
    env = os.environ.copy()
    env["OPENAI_API_KEY"] = "prompt-preview"  # pragma: allowlist secret
    env["CALL_RECORD_BACKEND"] = "webhook"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/preview_system_prompt.py",
            "--company-name",
            "Example HVAC",
            "--agent-name",
            "Nia",
            "--tone",
            "calm helpful",
            "--warmth",
            "warm",
            "--language",
            "English",
            "--accent",
            "neutral American",
        ],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=True,
    )

    prompt = result.stdout
    assert "Example HVAC" in prompt
    assert "Nia" in prompt
    assert "# Delivery Style" in prompt
    assert "Target tone: calm helpful." in prompt
    assert "save_call_record" in prompt
    assert "{company_name}" not in prompt
    assert "{agent_name}" not in prompt


def test_prompt_as_code_doc_locks_runtime_settings_boundary():
    doc = (ROOT / "docs" / "PROMPT_AS_CODE.md").read_text(encoding="utf-8")
    assert "Do not add industry YAML files" in doc
    assert "Do not store the main prompt" in doc
    assert "python scripts/preview_system_prompt.py" in doc
