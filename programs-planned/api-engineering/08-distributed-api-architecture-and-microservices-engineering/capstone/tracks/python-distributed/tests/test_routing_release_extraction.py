import unittest

from distributed_api.extraction import ExtractionPhase, StranglerRouter
from distributed_api.model import Unavailable, ValidationError
from distributed_api.release import VersionPolicy
from distributed_api.routing import Instance, ServiceRegistry


class RoutingReleaseExtractionTests(unittest.TestCase):
    def test_round_robin_and_health(self) -> None:
        registry = ServiceRegistry()
        registry.register(Instance("a", "control", "1.0"))
        registry.register(Instance("b", "control", "1.0"))
        chosen = [registry.choose("control").instance_id for _ in range(4)]
        self.assertEqual(chosen, ["a", "b", "a", "b"])
        registry.set_health("control", "a", False)
        self.assertEqual(registry.choose("control").instance_id, "b")

    def test_no_healthy_instance(self) -> None:
        registry = ServiceRegistry()
        registry.register(Instance("a", "control", "1.0", healthy=False))
        with self.assertRaises(Unavailable):
            registry.choose("control")

    def test_version_policy(self) -> None:
        policy = VersionPolicy()
        self.assertEqual(policy.classify("1.0", "1.1"), "compatible")
        self.assertEqual(
            policy.classify("1.1", "1.0"),
            "compatible-with-feature-disabled",
        )
        self.assertEqual(policy.classify("2.0", "1.1"), "reject")

    def test_shadow_compare_blocks_divergence(self) -> None:
        router = StranglerRouter(lambda value: value, lambda value: value + 1)
        router.transition(ExtractionPhase.SHADOW)
        self.assertEqual(router.call("k", 1), 1)
        self.assertFalse(router.shadow_clean())
        with self.assertRaises(ValidationError):
            router.transition(ExtractionPhase.CANARY, canary_fraction=0.1)

    def test_clean_shadow_canary_and_cutover(self) -> None:
        router = StranglerRouter(lambda value: value * 2, lambda value: value * 2)
        router.transition(ExtractionPhase.SHADOW)
        router.call("k", 2)
        self.assertTrue(router.shadow_clean())
        router.transition(ExtractionPhase.CANARY, canary_fraction=0.5)
        router.transition(ExtractionPhase.CUTOVER)
        self.assertEqual(router.call("k", 3), 6)

    def test_direct_shadow_to_cutover_is_rejected(self) -> None:
        router = StranglerRouter(lambda value: value, lambda value: value)
        router.transition(ExtractionPhase.SHADOW)
        router.call("k", 1)
        with self.assertRaises(ValidationError):
            router.transition(ExtractionPhase.CUTOVER)


if __name__ == "__main__":
    unittest.main()
