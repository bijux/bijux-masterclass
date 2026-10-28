from __future__ import annotations

import unittest

from fastapi import FastAPI
from fastapi.testclient import TestClient

from api_reliability.fastapi_adapter import install_reliability
from api_reliability.health import LifecycleController, LifecyclePhase


class FastAPIAdapterTests(unittest.TestCase):
    def build(self):
        app = FastAPI()
        lifecycle = LifecycleController()
        lifecycle.transition(
            LifecyclePhase.ACCEPTING,
            reason="test-ready",
            timestamp_ms=1,
        )

        @app.get("/ok", operation_id="getOk")
        async def ok():
            return {"status": "ok"}

        runtime = install_reliability(
            app,
            lifecycle=lifecycle,
            readiness_check=lambda: None,
            service_name="test-api",
            service_version="1.0.0",
            environment="test",
        )
        return app, runtime

    def test_internal_endpoints_are_hidden_and_request_is_measured(self) -> None:
        app, _ = self.build()
        with TestClient(app) as client:
            response = client.get("/ok", headers={"traceparent": "invalid"})
            self.assertEqual(response.status_code, 200)
            self.assertRegex(
                response.headers["traceparent"],
                r"^00-[0-9a-f]{32}-[0-9a-f]{16}-00$",
            )
            metrics = client.get("/internal/metrics")
            self.assertEqual(metrics.status_code, 200)
            self.assertIn('operation="getOk"', metrics.text)
            schema = client.get("/openapi.json").json()
            self.assertNotIn("/internal/metrics", schema["paths"])

    def test_draining_is_live_but_not_ready(self) -> None:
        app, runtime = self.build()
        with TestClient(app) as client:
            self.assertEqual(client.get("/internal/health/ready").status_code, 200)
            runtime.begin_drain(reason="test-drain")
            self.assertEqual(client.get("/internal/health/live").status_code, 200)
            self.assertEqual(client.get("/internal/health/ready").status_code, 503)


if __name__ == "__main__":
    unittest.main()
