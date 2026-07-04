"""Contracts for the Twilio Media Stream bridge and Realtime connection URL."""

import asyncio
import json
import os
import sys

from fastapi.websockets import WebSocketDisconnect
from starlette.requests import Request

# Ensure project root is on path.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config
from services.connection_manager import WebSocketConnectionManager
from services.twilio_service import TwilioService


def _request(method: str, host: str, body: bytes = b"") -> Request:
    async def receive() -> dict:
        return {"type": "http.request", "body": body, "more_body": False}

    return Request(
        {
            "type": "http",
            "method": method,
            "path": "/incoming-call",
            "headers": [(b"host", host.encode("ascii"))],
            "server": (host, 443),
            "scheme": "https",
            "query_string": b"",
        },
        receive,
    )


def test_incoming_twiml_uses_custom_parameter_for_caller_number():
    request = _request(
        "POST",
        "example.com",
        b"From=%2B15551234567&CallSid=CA123",
    )

    response = asyncio.run(TwilioService.create_incoming_call_response(request))
    xml = response.body.decode("utf-8")

    assert 'url="wss://example.com/media-stream"' in xml
    assert "?caller_number=" not in xml
    assert 'name="caller_number" value="+15551234567"' in xml


class _FakeTwilioWebSocket:
    def __init__(self, messages: list[dict]):
        self._messages = messages

    async def iter_text(self):
        for message in self._messages:
            yield json.dumps(message)


def test_stream_start_custom_parameters_hydrate_connection_state():
    manager = WebSocketConnectionManager(
        _FakeTwilioWebSocket(
            [
                {
                    "event": "start",
                    "start": {
                        "streamSid": "MZ123",
                        "callSid": "CA123",
                        "customParameters": {
                            "caller_number": "+15551234567",
                        },
                    },
                }
            ]
        )
    )
    starts: list[str] = []

    async def on_media(_: dict) -> None:
        raise AssertionError("media handler should not run")

    async def on_start(stream_sid: str) -> None:
        starts.append(stream_sid)

    async def on_mark() -> None:
        raise AssertionError("mark handler should not run")

    async def run() -> None:
        try:
            await manager.receive_from_twilio(on_media, on_start, on_mark)
        except WebSocketDisconnect:
            pass

    asyncio.run(run())

    assert starts == ["MZ123"]
    assert manager.state.stream_sid == "MZ123"
    assert manager.state.call_sid == "CA123"
    assert manager.state.caller_phone_number == "+15551234567"


def test_realtime_websocket_url_uses_model_only(monkeypatch):
    monkeypatch.setattr(Config, "OPENAI_REALTIME_MODEL", "gpt-realtime-2")
    monkeypatch.setattr(Config, "TEMPERATURE", 0.1)
    monkeypatch.setattr(Config, "VOICE", "cedar")

    url = Config.get_openai_websocket_url()

    assert url == "wss://api.openai.com/v1/realtime?model=gpt-realtime-2"
    assert "temperature=" not in url
    assert "voice=" not in url
