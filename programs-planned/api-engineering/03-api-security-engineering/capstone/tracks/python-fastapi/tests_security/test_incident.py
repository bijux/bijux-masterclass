import pytest

from api_security.incident import Incident, IncidentStatus, TimelineEntry


def test_incident_transitions_revocation_and_rotation():
    incident=Incident("INC-1")
    incident.record(TimelineEntry("2026-08-06T09:00:00Z","alert","fixture compromise","confirmed"))
    incident.transition(IncidentStatus.TRIAGED)
    incident.revoke_token("stolen-jti")
    incident.rotate_webhook_key("whk-2026-02",keep_old_for_verification=True)
    assert {"whk-2026-01","whk-2026-02"}<=incident.verification_keys
    incident.transition(IncidentStatus.CONTAINED)
    incident.retire_webhook_key("whk-2026-01")
    incident.transition(IncidentStatus.RECOVERED)
    incident.transition(IncidentStatus.CLOSED)
    assert "stolen-jti" in incident.revoked_token_ids


def test_illegal_incident_transition_rejected():
    with pytest.raises(ValueError):
        Incident("INC-2").transition(IncidentStatus.CLOSED)
