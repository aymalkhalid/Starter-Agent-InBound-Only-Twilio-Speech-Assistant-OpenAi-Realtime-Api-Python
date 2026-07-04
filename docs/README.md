# Voice Agent Starter Docs

Docs for the Twilio + OpenAI Realtime starter. Agent behavior is defined in `prompts/main_system_instructions.md`, rendered with env-driven placeholders from `config.py`, and aligned with OpenAI's Realtime prompting guide.

## Guides

- [Onboarding](./ONBOARDING.md) — one-page clone → live agent checklist
- [Prompt-as-code](./PROMPT_AS_CODE.md) — customize industries with code edits, prompt preview, and tests
- [Multi-client workflow](./MULTI_CLIENT_WORKFLOW.md) — build a separate agent per client (real estate, lead qualifier, etc.)
- [Client discovery template](./templates/CLIENT_DISCOVERY.md) — fillable kickoff form per new client
- [Architecture](./ARCHITECTURE.md)
- [Master diagram](./MASTER_DIAGRAM.md) — PNG poster + Mermaid source + step-by-step breakdown ([`images/MasterArchitectureDiagram.png`](./images/MasterArchitectureDiagram.png))
- [Diagrams](./DIAGRAMS.md) — Inbound Mermaid flows (7 sections)
- [Configuration](./CONFIGURATION.md) — prompt placeholders, tone/language/accent, reasoning effort, VAD, silence handling
- [Realtime Tools](./TOOLS.md)
- [Cloud Run Deploy](./DEPLOY_CLOUD_RUN.md)

## Prompting reference

- [OpenAI Realtime prompting guide (local copy)](./references/openai-realtime-models-prompting.md)
- [Starter prompt ↔ guide mapping](./references/STARTER_PROMPT_MAPPING.md)

## Database

Supabase SQL helpers live in `docs/supabase-schema/`; start with `call_records_schema.sql`.
