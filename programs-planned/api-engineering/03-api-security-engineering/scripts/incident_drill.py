#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

import yaml

from api_security.incident import Incident, IncidentStatus, TimelineEntry

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    scenario = yaml.safe_load((ROOT / "capstone" / "incident" / "scenario.yaml").read_text())
    incident = Incident(scenario["incidentId"])
    for fact in scenario["facts"]:
        incident.record(TimelineEntry(fact["at"], fact["source"], fact["statement"], fact["confidence"]))
    incident.transition(IncidentStatus.TRIAGED)
    incident.revoke_token("fixture-stolen-jti")
    incident.rotate_webhook_key("whk-2026-02", keep_old_for_verification=True)
    incident.transition(IncidentStatus.CONTAINED)
    incident.retire_webhook_key("whk-2026-01")
    incident.transition(IncidentStatus.RECOVERED)
    incident.transition(IncidentStatus.CLOSED)
    result = {
        "incidentId": incident.incident_id,
        "status": incident.status.value,
        "timelineRecords": len(incident.timeline),
        "revokedTokenIds": sorted(incident.revoked_token_ids),
        "activeWebhookKey": incident.active_webhook_key,
        "verificationKeys": sorted(incident.verification_keys),
        "secretValuesIncluded": False,
    }
    if result["status"] != "closed" or "fixture-stolen-jti" not in result["revokedTokenIds"] or "whk-2026-01" in result["verificationKeys"]:
        raise SystemExit("incident drill failed")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
