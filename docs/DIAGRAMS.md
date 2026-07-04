# Inbound Diagrams

This repo is an inbound-only Twilio + OpenAI Realtime starter.

## 1. Inbound Call Sequence

```mermaid
sequenceDiagram
    participant C as Caller
    participant T as Twilio Voice
    participant F as FastAPI
    participant O as OpenAI Realtime

    C->>T: Calls business number
    T->>F: POST /incoming-call
    F-->>T: TwiML Connect Stream
    T->>F: WS /media-stream
    F->>O: Realtime session.update
    F->>O: Initial greeting item
    loop Live call
        T->>F: caller audio frame
        F->>O: input_audio_buffer.append
        O->>F: response.audio.delta
        F->>T: media frame
    end
```

## 2. Prompt Pipeline

```mermaid
flowchart TD
    MD[prompts/main_system_instructions.md]
    CFG[config.py builders]
    SYS[system_instructions.py renderer]
    MSG[Config.SYSTEM_MESSAGE]
    RT[OpenAI Realtime session.update]

    MD --> SYS
    CFG --> SYS
    SYS --> MSG
    MSG --> RT
```

Injected placeholders include `{agent_name}`, `{company_name}`, `{delivery_instruction}`, `{language_instruction}`, `{accent_instruction}`, `{reasoning_effort_instruction}`, `{tools_availability_instruction}`, `{call_record_instruction}`, `{booking_instruction}`, and `{transfer_instruction}`.

## 3. Tool Layer

```mermaid
flowchart LR
    RT[OpenAI Realtime Tool Call] --> OpenAIService[services/openai_service.py]
    OpenAIService --> Wait[wait_for_user]
    OpenAIService --> End[end_call]
    OpenAIService --> Save[save_call_record]
    OpenAIService --> Booking[Calendar booking tools]
    OpenAIService --> Transfer[request_human_handoff]
```

## 4. End-Call Goodbye Flow

```mermaid
stateDiagram-v2
    [*] --> ActiveCall
    ActiveCall --> GoodbyeQueued: end_call tool
    GoodbyeQueued --> FarewellPlaying: response audio starts
    FarewellPlaying --> AudioHeard: audio done
    AudioHeard --> PlaybackDrained: Twilio marks drained
    PlaybackDrained --> Finalizing: tail buffer
    AudioHeard --> Finalizing: watchdog / fallback grace
    Finalizing --> Hangup: close Twilio WebSocket / REST hangup
```

## 5. Optional Post-Call Services

```mermaid
flowchart TD
    Call[Inbound call] --> Record[Optional Twilio recording]
    Record --> Transcribe[Optional transcription]
    Transcribe --> Enhance[Optional transcript enhancement]
    Call --> Save[save_call_record]
    Save --> Store[Webhook or Supabase]
    Enhance --> Store
    Store --> Dashboard[Optional dashboard]
```

## 6. Dynamic Settings Boundary

```mermaid
flowchart LR
    Dashboard[Dashboard Settings] --> AppSettings[Supabase app_settings]
    AppSettings --> Config[Runtime-safe Config overrides]
    Config --> Prompt[Rendered prompt sections]
```

Runtime-safe settings include voice, tone, warmth, expressiveness, pacing, language, accent, model, VAD, booking, transfer, recording, and dashboard state. Full prompts, industry profiles, and tool policy stay in code.

## 7. What Is Not In This Starter

No outbound campaign APIs, no contact-list dialer, no outbound TwiML endpoint, no outbound status callback, and no missed-call AI callback.
