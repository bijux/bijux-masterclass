"""Closed interactive workload used to contrast with open-arrival k6 profiles."""

from __future__ import annotations

import os
from locust import HttpUser, between, task


class AnalysisPlatformUser(HttpUser):
    wait_time = between(0.4, 1.2)

    def on_start(self) -> None:
        token = os.environ.get("ACCESS_TOKEN")
        if not token:
            raise RuntimeError("ACCESS_TOKEN must be explicit")
        self.client.headers.update({"Authorization": f"Bearer {token}"})

    @task(8)
    def list_runs(self) -> None:
        with self.client.get(
            "/analysis-runs?limit=20",
            name="GET /analysis-runs",
            catch_response=True,
        ) as response:
            if response.status_code != 200:
                response.failure(f"unexpected status {response.status_code}")
                return
            try:
                value = response.json()
            except ValueError as exc:
                response.failure(f"invalid JSON: {exc}")
                return
            if not isinstance(value.get("items"), list):
                response.failure("items is not a list")

    @task(2)
    def get_project(self) -> None:
        with self.client.get(
            "/projects/project-1",
            name="GET /projects/{projectId}",
            catch_response=True,
        ) as response:
            if response.status_code != 200:
                response.failure(f"unexpected status {response.status_code}")
