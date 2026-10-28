#!/usr/bin/env python3
from __future__ import annotations

import asyncio
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
PY_SRC = ROOT / "capstone/tracks/python-fastapi/src"
sys.path.insert(0, str(PY_SRC))

from event_engineering.envelope import EventEnvelope
from event_engineering.nats_adapter import to_nats_request


async def main() -> None:
    try:
        import nats
    except ImportError as exc:
        raise SystemExit(f"nats-py is required: {exc}")

    event_path = ROOT / "capstone/contracts/examples/analysis-run-completed.v1.json"
    event = EventEnvelope(**json.loads(event_path.read_text(encoding="utf-8")))
    request = to_nats_request("analysis.course6.run.completed", event)
    nc = await nats.connect(
        os.environ.get("NATS_URL", "nats://127.0.0.1:4222"),
        user=os.environ.get("NATS_USER", "analysis_control"),
        password=os.environ.get("NATS_PASSWORD", "fixture-control"),
    )
    try:
        js = nc.jetstream()
        try:
            await js.delete_stream("COURSE6")
        except Exception:
            pass
        await js.add_stream(name="COURSE6", subjects=["analysis.course6.>"])
        headers = dict(request.headers)
        headers["Nats-Msg-Id"] = request.message_id
        first = await js.publish(request.subject, request.payload, headers=headers)
        second = await js.publish(request.subject, request.payload, headers=headers)
        subscription = await js.pull_subscribe(
            request.subject,
            durable="course6-proof",
            stream="COURSE6",
        )
        [message] = await subscription.fetch(1, timeout=5)
        observed = json.loads(message.data)
        if observed["id"] != event.id:
            raise RuntimeError("live broker changed event identity")
        await message.ack()
        info = await js.stream_info("COURSE6")
        report = {
            "eventId": event.id,
            "firstSequence": first.seq,
            "secondSequence": second.seq,
            "streamMessages": info.state.messages,
            "deduplicatedWithinBrokerWindow": info.state.messages == 1,
        }
        print(json.dumps(report, indent=2, sort_keys=True))
    finally:
        await nc.drain()


if __name__ == "__main__":
    asyncio.run(main())
