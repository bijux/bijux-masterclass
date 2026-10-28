from fastapi.testclient import TestClient

from api_security.fastapi_adapter import create_security_demo_app


def test_strict_json_adapter_accepts_and_rejects():
    client=TestClient(create_security_demo_app())
    response=client.post("/security/strict-json",content=b'{"name":"ok"}',headers={"content-type":"application/json"})
    assert response.status_code==200 and response.json()["value"]=={"name":"ok"}
    response=client.post("/security/strict-json",content=b'{"role":"reader","role":"admin"}',headers={"content-type":"application/json"})
    assert response.status_code==400
    assert response.json()["type"].endswith("duplicate-key")
