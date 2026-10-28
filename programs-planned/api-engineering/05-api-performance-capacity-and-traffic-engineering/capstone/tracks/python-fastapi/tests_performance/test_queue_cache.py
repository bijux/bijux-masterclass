from __future__ import annotations

import asyncio
import unittest

from api_performance.admission import AdmissionRejected, FairAdmission
from api_performance.cache import AuthorizedCacheKey, BoundedTTLCache
from api_performance.queueing import (
    little_law,
    mean_time_from_little_law,
    mm1_approximation,
)
from api_performance.singleflight import SingleFlight, SingleFlightRejected


class QueueingTests(unittest.TestCase):
    def test_little_law(self) -> None:
        result = little_law(
            throughput_per_second=20,
            mean_time_seconds=5,
            unit="jobs",
        )
        self.assertEqual(result.mean_in_system, 100)
        self.assertEqual(
            mean_time_from_little_law(
                mean_in_system=320,
                throughput_per_second=10,
            ),
            32,
        )

    def test_mm1_knee(self) -> None:
        low = mm1_approximation(arrival_rate=80, service_rate=100)
        high = mm1_approximation(arrival_rate=95, service_rate=100)
        self.assertEqual(low.mean_time_seconds, 0.05)
        self.assertEqual(high.mean_time_seconds, 0.2)
        with self.assertRaises(ValueError):
            mm1_approximation(arrival_rate=100, service_rate=100)


class AdmissionTests(unittest.IsolatedAsyncioTestCase):
    async def test_global_and_key_limits(self) -> None:
        admission = FairAdmission(
            max_active=2,
            max_waiters=2,
            max_active_per_key=1,
        )
        permit_a = await admission.acquire("tenant-a")
        permit_b = await admission.acquire("tenant-b")
        snapshot = await admission.snapshot()
        self.assertEqual(snapshot.active, 2)
        task = asyncio.create_task(
            admission.acquire("tenant-a", timeout_seconds=0.01)
        )
        with self.assertRaises(AdmissionRejected):
            await task
        await permit_a.release()
        await permit_b.release()
        self.assertEqual((await admission.snapshot()).active, 0)

    async def test_waiter_capacity(self) -> None:
        admission = FairAdmission(
            max_active=1,
            max_waiters=1,
            max_active_per_key=1,
        )
        permit = await admission.acquire("a")
        waiter = asyncio.create_task(admission.acquire("b"))
        await asyncio.sleep(0)
        with self.assertRaises(AdmissionRejected) as caught:
            await admission.acquire("c")
        self.assertEqual(caught.exception.reason, "waiter-capacity")
        await permit.release()
        acquired = await waiter
        await acquired.release()

    async def test_double_release_rejected(self) -> None:
        admission = FairAdmission(
            max_active=1,
            max_waiters=0,
            max_active_per_key=1,
        )
        permit = await admission.acquire("a")
        await permit.release()
        with self.assertRaises(RuntimeError):
            await permit.release()


def key(version: str = "1", tenant: str = "t1") -> AuthorizedCacheKey:
    return AuthorizedCacheKey(
        tenant_id=tenant,
        policy_partition="owner",
        resource_type="project",
        resource_id="p1",
        version=version,
        representation="api-1.2",
    )


class CacheTests(unittest.TestCase):
    def test_key_partition(self) -> None:
        self.assertNotEqual(key(tenant="a").canonical, key(tenant="b").canonical)
        self.assertNotEqual(key("1").canonical, key("2").canonical)

    def test_ttl_and_lru(self) -> None:
        cache: BoundedTTLCache[str] = BoundedTTLCache(
            max_entries=2,
            max_bytes=100,
        )
        cache.put(key("1"), "a", now_ns=0, ttl_ns=10, size_bytes=10)
        self.assertEqual(cache.get(key("1"), now_ns=5).state, "hit")
        self.assertEqual(cache.get(key("1"), now_ns=10).state, "stale")
        cache.put(key("1"), "a", now_ns=0, ttl_ns=100, size_bytes=10)
        cache.put(key("2"), "b", now_ns=0, ttl_ns=100, size_bytes=10)
        cache.put(
            AuthorizedCacheKey("t1", "owner", "project", "p2", "1", "api-1.2"),
            "c",
            now_ns=0,
            ttl_ns=100,
            size_bytes=10,
        )
        self.assertEqual(cache.snapshot.entries, 2)
        self.assertEqual(cache.snapshot.evictions, 1)

    def test_oversized_value_not_cached(self) -> None:
        cache: BoundedTTLCache[str] = BoundedTTLCache(
            max_entries=2,
            max_bytes=10,
        )
        cache.put(key(), "x", now_ns=0, ttl_ns=10, size_bytes=20)
        self.assertEqual(cache.snapshot.entries, 0)


class SingleFlightTests(unittest.IsolatedAsyncioTestCase):
    async def test_one_origin_call(self) -> None:
        flight: SingleFlight[int] = SingleFlight(
            max_concurrent_fills=2,
            max_waiters_per_key=20,
        )
        calls = 0

        async def origin() -> int:
            nonlocal calls
            calls += 1
            await asyncio.sleep(0.01)
            return 7

        values = await asyncio.gather(
            *(flight.do("key", origin) for _ in range(10))
        )
        self.assertEqual(values, [7] * 10)
        self.assertEqual(calls, 1)
        self.assertEqual((await flight.snapshot())["fills"], 0)

    async def test_failed_fill_not_poisoned(self) -> None:
        flight: SingleFlight[int] = SingleFlight(
            max_concurrent_fills=1,
            max_waiters_per_key=2,
        )
        calls = 0

        async def failing() -> int:
            nonlocal calls
            calls += 1
            raise RuntimeError("origin")

        with self.assertRaises(RuntimeError):
            await flight.do("key", failing)
        self.assertEqual(await flight.do("key", lambda: asyncio.sleep(0, result=3)), 3)
        self.assertEqual(calls, 1)

    async def test_fill_capacity(self) -> None:
        flight: SingleFlight[int] = SingleFlight(
            max_concurrent_fills=1,
            max_waiters_per_key=2,
        )
        blocker = asyncio.Event()

        async def slow() -> int:
            await blocker.wait()
            return 1

        first = asyncio.create_task(flight.do("a", slow))
        await asyncio.sleep(0)
        with self.assertRaises(SingleFlightRejected):
            await flight.do("b", slow)
        blocker.set()
        self.assertEqual(await first, 1)


if __name__ == "__main__":
    unittest.main()
