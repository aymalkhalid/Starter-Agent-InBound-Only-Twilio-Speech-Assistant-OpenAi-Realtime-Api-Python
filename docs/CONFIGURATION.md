# Configuration

The starter uses environment variables, runtime config in `config.py`, and one editable prompt file.

## Main Prompt

Edit behavior in:

```text
prompts/main_system_instructions.md
```

At runtime, `config.py` renders placeholders and produces `Config.SYSTEM_MESSAGE` for the Realtime session.

### Static prompt sections

The markdown file defines OpenAI Realtime-aligned behavior:

- Role, conversation flow, reasoning, personality
- Preambles and verbosity
- Silence handling (`wait_for_user`) and unclear audio
- Entity capture (collection order, spelled-out values, spoken numbers, confirmation workflow)
- Instruction precision (avoid overly broad `always` / `must` rules)
- Tool eagerness, read/write rules, and failure recovery

### Injected placeholders

| Placeholder | Built by | Purpose |
| --- | --- | --- |
| `{company_name}` | `Config.COMPANY_NAME` | Business name |
| `{agent_name}` | `Config.AGENT_NAME` | Spoken agent name |
| `{delivery_instruction}` | `_build_delivery_instruction()` | Human delivery style: tone, warmth, expressiveness, pacing |
| `{language_instruction}` | `_build_language_instruction()` | English-primary or multilingual policy |
| `{accent_instruction}` | `_build_accent_instruction()` | English delivery accent, separate from language |
| `{reasoning_effort_instruction}` | `_build_reasoning_effort_instruction()` | gpt-realtime-2 effort guidance (empty for older models) |
| `{tools_availability_instruction}` | `_build_tools_availability_instruction()` | Lists tools actually enabled this session |
| `{call_record_instruction}` | `_build_call_record_instruction()` | When/how to call `save_call_record` |
| `{booking_instruction}` | `_build_booking_instruction()` | Booking flow and confirmation rules |
| `{transfer_instruction}` | `_build_transfer_instruction()` | Human handoff rules |

Change wording in the markdown file when possible. Change env vars when behavior depends on enabled features or voice/tone/language settings.

Reference: [Starter prompt ↔ guide mapping](./references/STARTER_PROMPT_MAPPING.md)

For industry/client changes, use the prompt-as-code workflow instead of storing full prompts in Supabase: [Prompt-as-code customization](./PROMPT_AS_CODE.md).

Preview the fully rendered Realtime instructions locally:

```bash
python scripts/preview_system_prompt.py
```

## Silence, background audio, and unclear speech

The prompt separates two cases (see `# Handling Silence and Background Noise` and `# Unclear Audio`):

| Caller audio | Model action |
| --- | --- |
| Not addressed to the agent (silence, hold music, TV, side talk) | Call `wait_for_user` — no spoken reply |
| Clearly addressed but ambiguous, noisy, or cut off | One brief clarification question — do not call `wait_for_user` |

Runtime support lives in `services/openai_service.py` and `main.py`: silent tool completion, audio suppression/truncation, and per-call `wait_for_user_count` logging. Details: [Realtime Tools](./TOOLS.md#wait_for_user-silence-and-background-audio).

## Voice activity detection (VAD)

VAD controls when OpenAI ends a user turn. It complements — but does not replace — `wait_for_user`.

| Variable | Default | Notes |
| --- | --- | --- |
| `VAD_MODE` | `server_vad` | `server_vad` (silence-based) or `semantic_vad` (content-based; often better in noisy environments) |
| `VAD_EAGERNESS` | `auto` | For `semantic_vad` only: `low`, `medium`, `high`, or `auto` |
| `VAD_THRESHOLD` | `0.6` | For `server_vad` only: higher = less sensitive to background noise (0–1) |
| `VAD_SILENCE_DURATION_MS` | `600` | For `server_vad` only: ms of silence before speech is considered stopped |
| `VAD_PREFIX_PADDING_MS` | `300` | Audio captured before detected speech start |
| `VAD_DEBOUNCE_AFTER_OUTGOING_MS` | `1200` | Ignore `speech_started` briefly after assistant audio (reduces echo triggers) |
| `VAD_INTERRUPTION_CONFIRM_MS` | `0` | Wait this many ms before truncating on interruption; `0` = immediate |

Example for a noisy phone line:

```env
VAD_MODE=semantic_vad
VAD_EAGERNESS=low
VAD_THRESHOLD=0.65
```

VAD can also be tuned from the dashboard Settings panel when Supabase is enabled.

## End-Call Goodbye Timing

When the model calls `end_call`, the server queues a farewell, waits for the farewell response to complete, then waits for Twilio playback marks before hanging up. If mark-based waiting is unavailable, it falls back to a fixed grace sleep.

| Variable | Default | Notes |
| --- | --- | --- |
| `END_CALL_DYNAMIC_MARKS` | `true` | Use Twilio mark callbacks to wait for farewell audio playback before hangup |
| `END_CALL_GRACE_SECONDS` | `6` | Maximum mark-drain wait; also fixed fallback sleep |
| `END_CALL_TAIL_SECONDS` | `0.75` | Small buffer after marks drain to avoid clipping the final syllable |
| `END_CALL_WATCHDOG_SECONDS` | `10` | Safety timeout if farewell audio or `response.done` stalls |

## Core Env

| Variable | Default | Notes |
| --- | --- | --- |
| `OPENAI_API_KEY` | — | Required |
| `COMPANY_NAME` | `Acme Voice Agent Demo` | Spoken business name |
| `AGENT_NAME` | — | Spoken agent name |
| `AGENT_LABEL` | `generic_voice_agent` | Internal label |
| `SYSTEM_INSTRUCTIONS_PATH` | `prompts/main_system_instructions.md` | Alternate prompt file |
| `OPENAI_REALTIME_MODEL` | `gpt-realtime-2` | Realtime model id |
| `REALTIME_REASONING_EFFORT` | `low` | `minimal` … `xhigh`; sent in session for `gpt-realtime-2` only |
| `VOICE` | `cedar` | OpenAI Realtime voice |
| `ASSISTANT_TONE` | `warm professional` | Short delivery target inserted into prompt |
| `ASSISTANT_WARMTH` | `warm` | `neutral`, `warm`, `very_warm` |
| `ASSISTANT_EXPRESSIVENESS` | `balanced` | `reserved`, `balanced`, `expressive` |
| `ASSISTANT_PACING` | `moderate` | `relaxed`, `moderate`, `brisk` |
| `TEMPERATURE` | `0.8` | Legacy compatibility value; not sent to GA Realtime sessions |

## Delivery, Language, And Accent

Delivery controls are runtime-safe prompt controls for phone tone, not a full prompt editor.

English is the primary language. Accent is configured separately and does not change the response language.

| Variable | Default | Notes |
| --- | --- | --- |
| `ASSISTANT_LANGUAGE` | `English` | Default response language |
| `ASSISTANT_ACCENT` | `neutral American` | e.g. `neutral British`, `neutral Australian` |
| `ASSISTANT_ACCENT_STRENGTH` | `light` | `none`, `light`, `moderate` |
| `LANGUAGE_SWITCH_POLICY` | `default_only` | `default_only` pins English; `explicit_or_substantive` allows multilingual switching |

Example — English with a British accent, no language switching:

```env
ASSISTANT_TONE=warm professional
ASSISTANT_WARMTH=warm
ASSISTANT_EXPRESSIVENESS=balanced
ASSISTANT_PACING=moderate
ASSISTANT_LANGUAGE=English
ASSISTANT_ACCENT=neutral British
ASSISTANT_ACCENT_STRENGTH=light
LANGUAGE_SWITCH_POLICY=default_only
```

## Optional Features

- **Call records:** `CALL_RECORD_BACKEND` (`webhook`, `supabase`, …), `WEBHOOK_URL`, `SUPABASE_URL`, `SUPABASE_KEY`, `SUPABASE_CALL_RECORD_TABLE=call_records`
- **Booking:** `BOOKING_ENABLED=true`, `GOOGLE_CALENDAR_ID`, `GOOGLE_CALENDAR_CREDENTIALS_JSON`
- **Recording:** `CALL_RECORDING_ENABLED=true`, `RECORDING_STATUS_CALLBACK_BASE_URL`
- **Transfer:** `HUMAN_TRANSFER_URL`, `HUMAN_TRANSFER_ENABLED`, `HUMAN_TRANSFER_DIAL_NUMBER`
- **Missed-call list:** `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_PHONE_NUMBER`

## Supabase Schema

Run `docs/supabase-schema/call_records_schema.sql` when enabling Supabase call-record storage. Existing deployments can point `SUPABASE_CALL_RECORD_TABLE` at an older `leads` table while migrating.

Supabase `app_settings` stores runtime-safe overrides only. Do not put full system prompts, industry prompt profiles, or tool policy in `app_settings`; keep those in code and review them with tests.

## Changing Behavior Safely

1. Edit `prompts/main_system_instructions.md` for conversational rules.
2. Edit `.env` for tone, language, accent, reasoning effort, and feature toggles.
3. Edit tool schemas/handlers in `services/openai_service.py` when tool args or side effects change.
4. Preview the rendered prompt with `python scripts/preview_system_prompt.py`.
5. Run `pytest tests/test_system_instructions.py` after prompt or config builder changes.
