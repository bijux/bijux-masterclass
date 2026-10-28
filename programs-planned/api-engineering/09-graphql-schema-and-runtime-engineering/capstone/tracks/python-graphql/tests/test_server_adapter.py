"""Exercise the optional server adapter with installed framework dependencies."""

import asyncio

import pytest

pytest.importorskip("strawberry")
pytest.importorskip("fastapi")
pytest.importorskip("httpx")

import httpx
from graph_api.adapters.strawberry_app import create_app


def test_server_adapter_serves_graphql_with_the_patched_framework():
    async def request():
        transport = httpx.ASGITransport(app=create_app())
        async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
            return await client.post("/graphql", json={"query": "{ __typename }"})

    response = asyncio.run(request())

    assert response.status_code == 200
    assert response.json() == {"data": {"__typename": "Query"}}
