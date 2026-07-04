# Onboarding

One-page path from clone to a working inbound phone agent, with optional features in order. Visual flows: [Diagrams](./DIAGRAMS.md).

---

## Step 1 — Minimum viable agent (~15 min)

| Step | Action | Verify |
| --- | --- | --- |
| 1 | `python3 -m venv env && source env/bin/activate && pip install -r requirements.txt` | Dependencies install |
| 2 | `cp .env.example .env` — set `OPENAI_API_KEY` | `python main.py` starts |
| 3 | Edit `prompts/main_system_instructions.md` (company tone, intake flow) | Prompt reflects your use case |
| 4 | Expose HTTPS: `ngrok http 5050` **or** `./scripts/deploy-cloudrun.sh` | Public URL reachable |
| 5 | Twilio Voice webhook → `{URL}/incoming-call` | Inbound call reaches AI |
| 6 | Place test call — greet, talk, say goodbye | Agent hangs up via `end_call` |

Diagram: [§1 Inbound call sequence](./DIAGRAMS.md#1-inbound-call-sequence)

**Building for a specific client?** [Prompt-as-code](./PROMPT_AS_CODE.md) · [Multi-client workflow](./MULTI_CLIENT_WORKFLOW.md) · [Client discovery template](./templates/CLIENT_DISCOVERY.md)

---

## Step 2 — Customize behavior

| What | Where |
| --- | --- |
| Conversation rules, tool policy, safety | `prompts/main_system_instructions.md` |
| Agent name, voice, language, accent | `.env` (`AGENT_NAME`, `VOICE`, `ASSISTANT_*`) |
| Tool schemas + side effects | `services/openai_service.py` |
| Greeting / farewell phrasing | `system_instructions.py` |

After prompt changes: `python scripts/preview_system_prompt.py` and `pytest tests/test_system_instructions.py`

Diagram: [§2 Prompt pipeline](./DIAGRAMS.md#2-prompt-pipeline) · Mapping: [STARTER_PROMPT_MAPPING.md](./references/STARTER_PROMPT_MAPPING.md)

---

## Step 3 — Optional features (enable in this order)

| Order | Feature | Required env / setup | Diagram |
| --- | --- | --- | --- |
| 1 | **Dashboard + call records** | `CALL_RECORD_BACKEND=supabase`, Supabase schema, `DASHBOARD_USERS` | [§5](./DIAGRAMS.md#5-optional-post-call-services) |
| 2 | **Google Calendar booking** | GCal service account JSON, `GOOGLE_CALENDAR_ID`, booking flags | [§3](./DIAGRAMS.md#3-tool-layer) |
| 3 | **Call recording** | `CALL_RECORDING_ENABLED`, `RECORDING_STATUS_CALLBACK_BASE_URL` | [§5](./DIAGRAMS.md#5-optional-post-call-services) |
| 4 | **Transcription** | `TRANSCRIPTION_MODEL` (e.g. `tiny`) | [§5](./DIAGRAMS.md#5-optional-post-call-services) |
| 5 | **Missed-call list** | Twilio creds + `TWILIO_PHONE_NUMBER`; Supabase only needed to persist handled state | [§5](./DIAGRAMS.md#5-optional-post-call-services) |
| 6 | **Dashboard runtime settings** | Supabase `app_settings` table | [§6](./DIAGRAMS.md#6-dynamic-settings-boundary) |

---

## Step 4 — Key files map

```
main.py                          HTTP/WS routes, Twilio orchestration
config.py + .env                 Env loading, prompt builders, feature flags
prompts/main_system_instructions.md   Agent behavior (edit first)
services/openai_service.py       Realtime session, tools, tool handlers
services/connection_manager.py   Twilio ↔ OpenAI WebSocket bridge
services/twilio_service.py       TwiML, caller cache, recording
services/call_records_service.py Call record facade
static/dashboard.html            Dashboard UI (optional)
```

Full module overview: [Architecture](./ARCHITECTURE.md)

---

## Step 5 — Verify

```bash
# Prompt rendering
pytest tests/test_system_instructions.py

# OpenAI service / tool helpers
pytest tests/test_openai_service.py
```

---

## Step 6 — Production deploy

```bash
./scripts/deploy-cloudrun.sh
```

Post-deploy:
- Twilio webhook → `{SERVICE_URL}/incoming-call`
- Recording: `RECORDING_STATUS_CALLBACK_BASE_URL={SERVICE_URL}`
- GCal on GCP: mount credentials via Cloud Run secrets (not local file path)

Diagram: [Master architecture](./MASTER_DIAGRAM.md)

---

## Extending tools (future)

Built-in tools live in `openai_service.py`. External/MCP tools use the scaffold (disabled in v1):

- `services/tool_registry.py` — register schemas + handlers
- `services/mcp_adapter.py` — MCP loader (no-op placeholder)

Diagram: [§3 Tool layer](./DIAGRAMS.md#3-tool-layer)
