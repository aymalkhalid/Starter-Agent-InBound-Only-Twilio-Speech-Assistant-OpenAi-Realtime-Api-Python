# Prompt-As-Code Customization

Use this starter as a code-first template. Keep agent behavior in versioned files, let an agentic coding tool edit the prompt and related code, and reserve Supabase settings for runtime-safe knobs.

## Source of truth

| Concern | Where it lives |
| --- | --- |
| Main conversation behavior | `prompts/main_system_instructions.md` |
| Greeting and farewell helpers | `system_instructions.py` |
| Dynamic prompt sections | `config.py` builders |
| Tool schemas and side effects | `services/openai_service.py` |
| Runtime-safe settings | `.env` or dashboard Settings backed by Supabase `app_settings` |

Do not add industry YAML files, prompt-profile tables, prompt-version tables, or a dashboard prompt CMS to the starter. Client or industry behavior should be changed through reviewed code edits.

## Agentic customization workflow

1. Create a client project from the starter, or make changes in the client repo.
2. Fill `docs/templates/CLIENT_DISCOVERY.md` for the target industry/client.
3. Ask the coding agent to update `prompts/main_system_instructions.md` first.
4. Change `.env` or dashboard Settings for voice, tone, warmth, expressiveness, pacing, language, accent, model, VAD, booking, transfer, and recording.
5. Change tool schemas/handlers only when the prompt cannot express the required side effect.
6. Preview the rendered prompt:

```bash
python scripts/preview_system_prompt.py
```

7. Run focused verification:

```bash
pytest tests/test_system_instructions.py
```

8. Review the rendered prompt and place test calls before deployment.

## Industry checklist

Before editing the prompt, define:

- Role and objective: what the agent is and what a successful call means.
- Conversation flow: first question, intake order, and when to stop asking.
- Required intake fields: name, phone, issue, address, budget, timeline, or other industry values.
- Booking rules: whether booking is enabled, what can be booked, and what must be confirmed.
- Call-record rules: when to save, what summary should include, and what priority means.
- Transfer rules: when to hand off and what information to collect first.
- Greeting, farewell, and delivery: default `.env` wording/tone controls or custom helper changes.
- Tool behavior: which actions require confirmation and which are read-only lookups.

## Prompt patch examples

These are prompt-edit directions for a coding agent, not runtime profile files.

| Industry | Prompt patch direction |
| --- | --- |
| Real estate | Change role to showing/lead intake assistant; collect buyer/seller intent, property interest, budget range, timeline, preferred areas, and desired showing time. |
| Healthcare intake | Keep medical-safety boundaries explicit; collect symptom summary, urgency, callback details, preferred appointment time, and route emergencies to human/urgent care wording. |
| Home services | Collect service type, address, urgency, access notes, callback number, and whether the issue is emergency/same-day/routine. |
| Legal intake | Avoid legal advice; collect matter type, jurisdiction/location, opposing party if needed, urgency, and callback details before saving or transferring. |
| Restaurant booking | Collect party size, date, time, name, phone, special requests, and confirm the exact reservation details before booking. |
| Support triage | Collect account/product context, issue summary, impact, troubleshooting already tried, priority, and transfer when the prompt-defined threshold is met. |

## Supabase boundary

Supabase `app_settings` is for operational knobs that are safe to change without code review: voice, tone, warmth, expressiveness, pacing, language, accent, VAD, model choice, booking settings, transfer toggles, recording, and dashboard-related settings.

Do not store the main prompt, full system instructions, industry templates, or tool policy in Supabase for this starter. That keeps Realtime behavior predictable, testable, and easy to review in git.
