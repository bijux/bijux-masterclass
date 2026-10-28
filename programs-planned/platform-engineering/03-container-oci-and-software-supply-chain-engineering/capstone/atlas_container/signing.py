from __future__ import annotations

import base64
import hashlib
import json
from typing import Any

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey

from .canonical import canonical_json_bytes


def fixture_private_key() -> Ed25519PrivateKey:
    seed = hashlib.sha256(b"ATLAS COURSE FIXTURE KEY - NOT FOR DEPLOYMENT").digest()
    return Ed25519PrivateKey.from_private_bytes(seed)


def public_key_pem(key: Ed25519PublicKey) -> bytes:
    return key.public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo)


def private_key_pem(key: Ed25519PrivateKey) -> bytes:
    return key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption(),
    )


def key_fingerprint(key: Ed25519PublicKey) -> str:
    der = key.public_bytes(serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo)
    return "sha256:" + hashlib.sha256(der).hexdigest()


def _pae(payload_type: str, payload: bytes) -> bytes:
    type_bytes = payload_type.encode()
    return b"DSSEv1 %d %s %d " % (len(type_bytes), type_bytes, len(payload)) + payload


def sign_statement(statement: dict[str, Any], key: Ed25519PrivateKey, payload_type: str = "application/vnd.in-toto+json") -> dict[str, Any]:
    payload = canonical_json_bytes(statement)
    signature = key.sign(_pae(payload_type, payload))
    return {
        "payloadType": payload_type,
        "payload": base64.b64encode(payload).decode(),
        "signatures": [
            {
                "keyid": key_fingerprint(key.public_key()),
                "sig": base64.b64encode(signature).decode(),
            }
        ],
    }


def verify_envelope(
    envelope: dict[str, Any],
    key: Ed25519PublicKey,
    expected_keyid: str | None = None,
    expected_payload_type: str | None = None,
) -> dict[str, Any]:
    payload_type = envelope["payloadType"]
    if expected_payload_type is not None and payload_type != expected_payload_type:
        raise ValueError("envelope payload type does not match policy")
    payload = base64.b64decode(envelope["payload"], validate=True)
    signatures = envelope.get("signatures", [])
    if len(signatures) != 1:
        raise ValueError("expected exactly one signature")
    signature = signatures[0]
    keyid = key_fingerprint(key)
    if expected_keyid is not None and keyid != expected_keyid:
        raise ValueError("trusted key identity does not match policy")
    if signature.get("keyid") != keyid:
        raise ValueError("envelope key identifier mismatch")
    key.verify(base64.b64decode(signature["sig"], validate=True), _pae(payload_type, payload))
    value = json.loads(payload)
    if not isinstance(value, dict):
        raise ValueError("signed payload must be a JSON object")
    return value
