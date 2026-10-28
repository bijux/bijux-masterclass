from api_security.audit import AuditChain, AuditEvent, pseudonym
from api_security.secrets import SecretBytes, redact


def test_secret_never_renders():
    secret=SecretBytes("canary-secret-value")
    assert "canary" not in repr(secret)
    assert str(secret)=="[REDACTED]"


def test_shared_redaction_vectors(vector_loader):
    for case in vector_loader("redaction.json")["cases"]:
        assert redact(case["input"])==case["expected"],case["id"]


def test_audit_chain_and_tamper_detection():
    key=SecretBytes("audit-key")
    chain=AuditChain(key)
    chain.append(AuditEvent(1,"2026-08-06T12:00:00Z",pseudonym("user-1",key),"run.create","run:1","allow","policy.allow","req-1",{"authorization":"Bearer abc.def.ghi"}))
    chain.append(AuditEvent(2,"2026-08-06T12:01:00Z",pseudonym("user-1",key),"artifact.read","artifact:2","deny","tenant.foreign","req-2",{}))
    assert chain.verify()
    assert chain.records[0]["context"]["authorization"]=="[REDACTED]"
    chain.records[0]["reason"]="changed"
    assert not chain.verify()
