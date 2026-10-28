from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class AsyncAPIProfileReport:
    operation_count: int
    channel_count: int
    message_count: int


class AsyncAPIProfileError(ValueError):
    pass


def validate_course_profile(document: dict[str, Any]) -> AsyncAPIProfileReport:
    if document.get("asyncapi") != "3.1.0":
        raise AsyncAPIProfileError("expected AsyncAPI 3.1.0")
    info = document.get("info")
    if not isinstance(info, dict) or not info.get("title") or not info.get("version"):
        raise AsyncAPIProfileError("info title/version required")
    channels = document.get("channels")
    operations = document.get("operations")
    components = document.get("components")
    if not isinstance(channels, dict) or not channels:
        raise AsyncAPIProfileError("channels required")
    if not isinstance(operations, dict) or not operations:
        raise AsyncAPIProfileError("operations required")
    if not isinstance(components, dict):
        raise AsyncAPIProfileError("components required")
    seen_channels = set(channels)
    for operation_id, operation in operations.items():
        if operation.get("action") not in {"send", "receive"}:
            raise AsyncAPIProfileError(
                f"operation {operation_id} has invalid action"
            )
        channel_ref = operation.get("channel", {}).get("$ref", "")
        if not channel_ref.startswith("#/channels/"):
            raise AsyncAPIProfileError(
                f"operation {operation_id} must reference a local channel"
            )
        channel_name = channel_ref.split("/")[-1]
        if channel_name not in seen_channels:
            raise AsyncAPIProfileError(
                f"operation {operation_id} references unknown channel"
            )
    messages: set[str] = set()
    for channel_name, channel in channels.items():
        if not isinstance(channel, dict) or not channel.get("address"):
            raise AsyncAPIProfileError(f"channel {channel_name} lacks address")
        for message in channel.get("messages", {}).values():
            ref = message.get("$ref", "") if isinstance(message, dict) else ""
            if not ref:
                raise AsyncAPIProfileError(
                    f"channel {channel_name} has inline/invalid message"
                )
            messages.add(ref)
    return AsyncAPIProfileReport(len(operations), len(channels), len(messages))
