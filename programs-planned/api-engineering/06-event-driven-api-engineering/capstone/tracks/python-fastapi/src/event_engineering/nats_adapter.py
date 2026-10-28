from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .envelope import EventEnvelope


@dataclass(frozen=True, slots=True)
class NatsPublishRequest:
    subject: str
    payload: bytes
    headers: dict[str, str]
    message_id: str


def to_nats_request(subject: str, event: EventEnvelope) -> NatsPublishRequest:
    if not subject or " " in subject:
        raise ValueError("invalid NATS subject")
    return NatsPublishRequest(
        subject=subject,
        payload=event.canonical_bytes(),
        headers={
            "Content-Type": "application/cloudevents+json",
            "X-Event-Type": event.type,
            "X-Tenant-Id": event.tenantid,
        },
        message_id=event.id,
    )


async def publish_jetstream(client: Any, request: NatsPublishRequest) -> Any:
    """Optional adapter; imports remain outside dependency-light proof."""
    return await client.publish(
        request.subject,
        request.payload,
        headers=request.headers,
        msg_id=request.message_id,
    )
