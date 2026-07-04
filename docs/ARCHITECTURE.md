# Architecture

## Runtime Flow

1. Twilio calls `/incoming-call`.
2. FastAPI returns TwiML that connects audio to `/media-stream`.
3. `main.py` creates a `ConnectionManager` and `OpenAIService`.
4. `OpenAIService` sends `Config.SYSTEM_MESSAGE` plus tool schemas to OpenAI Realtime.
5. Twilio audio frames and OpenAI audio deltas are bridged until the call ends.

### Non-addressed audio (`wait_for_user`)

When the model decides incoming audio does not need a reply:

1. It calls `wait_for_user` (tool schema in `openai_service.py`).
2. The handler completes the tool silently (`trigger_response=False`).
3. `main.py` may truncate/clear assistant filler audio and suppress further deltas for that turn.
4. Normal responses resume when the caller clearly addresses the agent again.

See [Realtime Tools](./TOOLS.md#wait_for_user-silence-and-background-audio).

## Main Modules

- `main.py`: HTTP/WebSocket routes and Twilio orchestration.
- `config.py`: env loading, delivery/language/accent/reasoning builders, and `Config.SYSTEM_MESSAGE` rendering.
- `system_instructions.py`: prompt file loading, greeting, and farewell text.
- `services/openai_service.py`: Realtime session payloads, tools, and function-call handling.
- `services/call_records_service.py`: generic call-record facade used by app code.
- `services/webhook_service.py`: compatibility storage adapter for webhook/Supabase writes.
- `services/google_calendar_booking_service.py`: optional calendar tools.
- `services/missed_calls_service.py`: optional inbound missed-call listing and handled-state tracking.
- `services/tool_registry.py` and `services/mcp_adapter.py`: future external tool integration.

## Prompt Pipeline

1. `prompts/main_system_instructions.md` holds static Realtime behavior rules.
2. `config.build_system_message()` injects placeholders (language, accent, reasoning effort, enabled tools, booking/transfer/record instructions).
3. `OpenAISessionManager.create_session_update()` sends instructions plus tool schemas to OpenAI Realtime.
4. For `gpt-realtime-2`, `REALTIME_REASONING_EFFORT` is also set on the session payload.

See [Configuration](./CONFIGURATION.md) and [Starter prompt mapping](./references/STARTER_PROMPT_MAPPING.md).

## Diagrams

Visual flows live in [Diagrams](./DIAGRAMS.md). For a single shareable overview, see [Master diagram](./MASTER_DIAGRAM.md). Quick start: [Onboarding](./ONBOARDING.md).
