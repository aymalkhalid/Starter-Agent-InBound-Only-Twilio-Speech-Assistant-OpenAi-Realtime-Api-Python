# OpenAI Realtime + Twilio Voice Agent Starter

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

Production-ready **Python/FastAPI** starter for inbound **phone AI agents**. [Twilio Media Streams](https://www.twilio.com/docs/voice/media-streams) bridge live caller audio to the [OpenAI Realtime API](https://platform.openai.com/docs/guides/realtime); you customize behavior in one markdown prompt and wire side effects through Python tool handlers.

**Repository:** [github.com/aymalkhalid/Starter-Agent-InBound-Only-Twilio-Speech-Assistant-OpenAi-Realtime-Api-Python](https://github.com/aymalkhalid/Starter-Agent-InBound-Only-Twilio-Speech-Assistant-OpenAi-Realtime-Api-Python)

---

## Architecture

One **WebSocket media bridge** (`/media-stream`) powers inbound calls from Twilio. Optional layers—Supabase CRM, Google Calendar booking, human transfer, recording, and transcription—attach via Realtime tools and env config.

<p align="center">
  <a href="./docs/MASTER_DIAGRAM.md">
    <img
      src="docs/images/MasterArchitectureDiagram.png"
      alt="Voice Agent Starter master architecture: inbound call trigger, WebSocket media bridge, Supabase CRM, Google Calendar, and optional post-call services"
      width="900"
    />
  </a>
</p>

<p align="center"><sub>Click the diagram for the full breakdown and Mermaid source · <a href="./docs/MASTER_DIAGRAM.md">docs/MASTER_DIAGRAM.md</a></sub></p>

| Layer | Required | What it does |
| --- | --- | --- |
| Twilio + OpenAI Realtime | Yes | Phone audio ↔ speech AI (`OPENAI_API_KEY` + Twilio webhook) |
| Inbound | Yes (default) | Caller → `/incoming-call` → `/media-stream` → default system prompt |
| Supabase CRM | Optional | Call records, dashboard, runtime settings |
| Webhook CRM | Optional | `save_call_record` POST to `WEBHOOK_URL` (no dashboard) |
| Google Calendar | Optional | Five booking tools when `BOOKING_ENABLED=true` |
| Post-call | Optional | Twilio recording + faster-whisper transcription (dashboard-triggered) |

**Diagram source & breakdown:** [docs/MASTER_DIAGRAM.md](./docs/MASTER_DIAGRAM.md) · **Detailed flows:** [docs/DIAGRAMS.md](./docs/DIAGRAMS.md) · **Module narrative:** [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md)

---

## Features

### Core (works with `OPENAI_API_KEY` only)

- Twilio ↔ OpenAI Realtime audio bridge over WebSocket
- Voice selection, VAD, barge-in, and preemptive session renewal
- OpenAI-aligned silence handling via `wait_for_user`
- Context-aware `end_call` goodbyes
- Single editable prompt: `prompts/main_system_instructions.md` (Realtime 2-aligned)

### Built-in tools

| Tool | When available |
| --- | --- |
| `wait_for_user`, `end_call` | Always |
| `save_call_record` | Call-record backend configured |
| `request_human_handoff` | Live transfer configured |
| Booking tools (5) | Google Calendar + booking enabled |

### Optional (env-gated)

- Supabase call-record **dashboard** (`/dashboard`, `/calls`)
- **Google Calendar** appointment booking
- Call **recording**, playback proxy, and **Whisper** transcription
- Dashboard **runtime settings** (voice, VAD, booking) via Supabase
- MCP / external tool registry scaffold (disabled in v1)

---

## Quick start

**Prerequisites:** Python 3.10+, [OpenAI API key](https://platform.openai.com/api-keys), [Twilio account](https://www.twilio.com/) with a Voice number, and a public HTTPS URL (ngrok or Cloud Run).

```bash
git clone https://github.com/aymalkhalid/Starter-Agent-InBound-Only-Twilio-Speech-Assistant-OpenAi-Realtime-Api-Python.git
cd Starter-Agent-InBound-Only-Twilio-Speech-Assistant-OpenAi-Realtime-Api-Python

python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Set `OPENAI_API_KEY` in `.env`, then run:

```bash
python main.py
```

Point your Twilio Voice webhook to:

```text
https://YOUR_PUBLIC_HOST/incoming-call
```

**Full checklist (MVP → optional features):** [docs/ONBOARDING.md](./docs/ONBOARDING.md)

---

## Customize the agent

| Goal | Edit |
| --- | --- |
| Conversation behavior | `prompts/main_system_instructions.md` |
| Tool schemas + handlers | `services/openai_service.py` |
| Voice, tone, language, accent, reasoning | `.env` or dashboard Settings (see [CONFIGURATION.md](./docs/CONFIGURATION.md)) |
| Greeting / farewell phrasing | `system_instructions.py` |

Prompting follows the [OpenAI Realtime guide](./docs/references/openai-realtime-models-prompting.md). Section mapping: [STARTER_PROMPT_MAPPING.md](./docs/references/STARTER_PROMPT_MAPPING.md).

For client or industry builds, keep behavior as prompt-as-code: use an agentic coding tool to edit the prompt and related tests/docs, then preview the rendered instructions before deploying:

```bash
python scripts/preview_system_prompt.py
pytest tests/test_system_instructions.py
```

Workflow: [PROMPT_AS_CODE.md](./docs/PROMPT_AS_CODE.md).

Example env values:

```env
COMPANY_NAME=Acme Voice Agent Demo
AGENT_NAME=Alex
OPENAI_REALTIME_MODEL=gpt-realtime-2
REALTIME_REASONING_EFFORT=low
VOICE=cedar
ASSISTANT_TONE=warm professional
ASSISTANT_WARMTH=warm
ASSISTANT_EXPRESSIVENESS=balanced
ASSISTANT_PACING=moderate
ASSISTANT_LANGUAGE=English
ASSISTANT_ACCENT=neutral American
ASSISTANT_ACCENT_STRENGTH=light
LANGUAGE_SWITCH_POLICY=default_only
```

---

## Documentation

| Guide | Description |
| --- | --- |
| [MASTER_DIAGRAM.md](./docs/MASTER_DIAGRAM.md) | Master architecture (PNG + Mermaid + step-by-step breakdown) |
| [ONBOARDING.md](./docs/ONBOARDING.md) | Clone → live agent checklist |
| [PROMPT_AS_CODE.md](./docs/PROMPT_AS_CODE.md) | Code-first prompt customization workflow |
| [MULTI_CLIENT_WORKFLOW.md](./docs/MULTI_CLIENT_WORKFLOW.md) | Separate deploy per client (real estate, lead qualifier, …) |
| [DIAGRAMS.md](./docs/DIAGRAMS.md) | Inbound architecture Mermaid diagrams |
| [ARCHITECTURE.md](./docs/ARCHITECTURE.md) | Module overview and runtime flow |
| [CONFIGURATION.md](./docs/CONFIGURATION.md) | Env vars and prompt placeholders |
| [TOOLS.md](./docs/TOOLS.md) | Realtime tool behavior |
| [DEPLOY_CLOUD_RUN.md](./docs/DEPLOY_CLOUD_RUN.md) | Production deploy |

---

## Dashboard and storage

The core phone agent runs **without Supabase**. To enable the dashboard, call records, recordings, and transcripts:

```env
CALL_RECORD_BACKEND=supabase
SUPABASE_URL=...
SUPABASE_KEY=...
DASHBOARD_USERS=admin:your-secure-password
```

Default table: `call_records`. Legacy `leads` tables: set `SUPABASE_CALL_RECORD_TABLE=leads`.

Schema: [docs/supabase-schema/](./docs/supabase-schema/)

---

## Deploy to Cloud Run

```bash
./scripts/deploy-cloudrun.sh
```

Reads local `.env`, excludes local file-path secrets, and deploys the `speech-assistant` service. Post-deploy: set Twilio webhook to `{SERVICE_URL}/incoming-call`.

Details: [docs/DEPLOY_CLOUD_RUN.md](./docs/DEPLOY_CLOUD_RUN.md)

---

## Project structure

```text
main.py                          # FastAPI routes, Twilio WebSocket bridge
config.py                        # Env loading, prompt builders
prompts/main_system_instructions.md   # Agent behavior (edit first)
services/openai_service.py       # Realtime session, tools, handlers
services/connection_manager.py   # Twilio ↔ OpenAI WebSocket manager
services/twilio_service.py       # TwiML, caller cache, recording
static/dashboard.html            # Optional call-record UI
docs/                            # Onboarding, diagrams, configuration
docs/images/MasterArchitectureDiagram.png  # Master architecture poster
```

---

## Development

```bash
pytest tests/test_system_instructions.py
pytest tests/test_openai_service.py
```

Pre-commit hooks scan for secrets (see `.pre-commit-config.yaml`).

---

## License

[MIT](LICENSE) — see [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for community guidelines.
