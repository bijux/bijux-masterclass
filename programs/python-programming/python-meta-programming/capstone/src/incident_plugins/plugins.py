from __future__ import annotations

import json

from .actions import action
from .fields import BooleanField, ChoiceField, IntegerField, StringField
from .framework import PluginBase


class DeliveryPlugin(PluginBase):
    """Abstract base for incident-delivery adapters."""

    __abstract__ = True
    group = "delivery"


class ConsoleNotifier(DeliveryPlugin):
    """Render an incident into a terminal-friendly line."""

    plugin_name = "console"

    prefix = StringField(default="[incident]", description="Prefix prepended to every rendered line.")
    stream = ChoiceField(
        "stdout",
        "stderr",
        default="stdout",
        description="Logical output stream for operational routing.",
    )
    uppercase_severity = BooleanField(
        default=False,
        description="Uppercase the severity token before rendering.",
    )

    @action("Render an incident for terminal delivery.")
    def deliver(self, *, title: str, severity: str, summary: str) -> str:
        label = severity.upper() if self.uppercase_severity else severity.lower()
        return f"{self.prefix} {label} {title}: {summary}"


class WebhookNotifier(DeliveryPlugin):
    """Build the request payload that would be posted to an HTTPS endpoint."""

    plugin_name = "webhook"

    endpoint = StringField(description="Destination HTTPS endpoint.", min_length=8)
    timeout_seconds = IntegerField(
        default=5,
        description="Request timeout budget in seconds.",
        minimum=1,
        maximum=60,
    )
    redact_summary = BooleanField(
        default=False,
        description="Replace the human summary with a constant placeholder.",
    )

    @action("Build a deterministic webhook payload.")
    def deliver(self, *, title: str, severity: str, summary: str) -> dict[str, object]:
        body = "[redacted]" if self.redact_summary else summary
        return {
            "endpoint": self.endpoint,
            "timeout_seconds": self.timeout_seconds,
            "payload": {
                "title": title,
                "severity": severity.lower(),
                "summary": body,
            },
        }


class PagerNotifier(DeliveryPlugin):
    """Produce the compact payload shape typically sent to paging systems."""

    plugin_name = "pager"

    service = StringField(description="Pager service integration identifier.", min_length=2)
    routing_key = StringField(description="Escalation routing key.", min_length=4)
    deduplicate = BooleanField(
        default=True,
        description="Emit a stable deduplication key for repeated incidents.",
    )

    @action("Build a paging payload with an optional deduplication key.")
    def deliver(self, *, title: str, severity: str, summary: str) -> dict[str, object]:
        event = {
            "service": self.service,
            "routing_key": self.routing_key,
            "title": title,
            "severity": severity.lower(),
            "summary": summary,
        }
        if self.deduplicate:
            event["dedup_key"] = f"{self.service}:{severity.lower()}:{title}".replace(" ", "-")
        return event

    @action("Produce a JSON preview for debugging and documentation.")
    def preview(self, *, title: str, severity: str, summary: str) -> str:
        return json.dumps(self.deliver(title=title, severity=severity, summary=summary), sort_keys=True)
