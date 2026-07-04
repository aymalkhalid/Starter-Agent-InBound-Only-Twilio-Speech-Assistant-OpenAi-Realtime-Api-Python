# Client discovery template

Copy this into a doc or ticket per client **before** cloning the starter. Fill every section; use the mapping table at the bottom to decide what to change in `.env` vs the prompt.

**Client name:** ___________________  
**Project slug (repo name):** ___________________  
**Date:** ___________________

---

## 1. Business context

| Field | Answer |
| --- | --- |
| Company name (spoken) | |
| Agent name (spoken) | |
| Industry / use case (e.g. real estate, lead qualifier, dental intake) | |
| Inbound call type (support, intake, booking, triage, etc.) | |
| Who calls? (customers, leads, patients, tenants, etc.) | |

---

## 2. Call goals

Check all that apply and add notes:

- [ ] Answer FAQs only (no save required)
- [ ] Capture lead / intake for follow-up
- [ ] Qualify leads (hot / warm / cold)
- [ ] Book appointments / showings
- [ ] Transfer hot leads to a human
- [ ] Other: ___________________

**Primary success metric:** What makes this call a win? (e.g. "qualified lead saved with budget + timeline", "showing booked", "FAQ answered in under 2 min")

**What should never happen?** (e.g. quote prices, give legal advice, promise same-day service)

---

## 3. Conversation script (high level)

**Opening:** How should the agent greet? (or use default from `COMPANY_NAME` + `AGENT_NAME`)

**Core questions (in order, one at a time):**

1.
2.
3.
4.
5.

**When to save a record:** After which info is collected?

**When to book:** What triggers scheduling?

**When to transfer:** What qualifies a handoff?

**When to end call:** Goodbye triggers only, or also after save?

---

## 4. Data to capture

List fields the business needs. Mark where each goes:

| Field | Required? | Maps to |
| --- | --- | --- |
| Name | | `save_call_record.contact_name` |
| Phone | | `save_call_record.contact_phone` |
| Email | | `save_call_record.contact_email` |
| Reason / issue | | `save_call_record.issue_summary` |
| Priority (hot/normal/urgent) | | `save_call_record.priority` |
| Full call narrative | | `save_call_record.call_summary` |
| Address / location | | `save_call_record.service_address` |
| Preferred callback time | | `save_call_record.preferred_callback_time` |
| Custom field: _________ | | Prompt text → `issue_summary` or `call_summary` unless schema extended |

**Confirm digit-by-digit:** Phone? Email? Reference codes?

---

## 5. Integrations and features

Check what this client needs:

| Feature | Needed? | Notes |
| --- | --- | --- |
| Save leads (`save_call_record`) | | Requires `WEBHOOK_URL` or Supabase |
| Dashboard (`/dashboard`) | | Supabase + schema + `DASHBOARD_USERS` |
| Google Calendar booking | | `BOOKING_ENABLED` + calendar creds |
| Live transfer to human | | `HUMAN_TRANSFER_URL` + dial number + Twilio creds |
| Call recording + transcript | | `CALL_RECORDING_ENABLED` + public callback URL |
| Missed-call list | | Twilio creds + `TWILIO_PHONE_NUMBER` |
| CRM / webhook URL | | |
| Custom API (MLS, CRM lookup) | | Needs new tool in `openai_service.py` |

---

## 6. Voice and language

| Setting | Value |
| --- | --- |
| Voice (`VOICE`) | e.g. `cedar`, `marin` |
| Language (`ASSISTANT_LANGUAGE`) | Default `English` |
| Accent (`ASSISTANT_ACCENT`) | e.g. `neutral American` |
| Multilingual callers? | `default_only` or `explicit_or_substantive` |
| Reasoning effort | `low` (typical for phone) |

**Custom greeting env (optional):** `WELCOME_MESSAGE` or `GREETING`

---

## 7. Deploy and ops

| Item | Value |
| --- | --- |
| Twilio phone number | |
| Deploy target (Cloud Run service name / host) | |
| `AGENT_LABEL` (tags records) | e.g. `acme_realty` |
| Who reviews call records? | |
| Test numbers for UAT | |

---

## 8. Discovery → implementation map

After filling sections 1–7, apply changes in this order:

| Discovery section | Step | File / env |
| --- | --- | --- |
| 1 Business context | 2–3 | Clone repo; `COMPANY_NAME`, `AGENT_NAME`, `AGENT_LABEL` |
| 2 Call goals | 4 | `# Role and Objective`, `# Conversation Flow`, `# Safety` |
| 3 Conversation script | 4 | `# Conversation Flow`, `# Tools` |
| 4 Data to capture | 4 | `# Entity Capture`; tool fields in `save_call_record` |
| 5 Integrations | 3 | `.env` feature flags (see [Configuration](../CONFIGURATION.md)) |
| 6 Voice and language | 3, 5 | `.env` voice/accent; optional `WELCOME_MESSAGE` |
| 7 Deploy and ops | 7 | Twilio webhook, Cloud Run, ngrok for dev |

**Do not customize in the starter repo** — use a client clone. See [Multi-client workflow](../MULTI_CLIENT_WORKFLOW.md).

---

## 9. Sign-off

- [ ] Client approved conversation script
- [ ] Integrations and credentials ready
- [ ] Discovery mapped to env + prompt sections
- [ ] Ready to clone and implement
