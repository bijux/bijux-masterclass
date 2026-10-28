import unittest

from atlas_net.cni import CNIState


class CNITests(unittest.TestCase):
    def test_add_replay_delete(self) -> None:
        state = CNIState("10.244.1.0/29")
        first = state.add(
            network="atlas",
            attachment_id="a1",
            container_id="c1",
            pod_uid="pod-a:uid1",
            interface="eth0",
            generation=1,
        )
        replay = state.add(
            network="atlas",
            attachment_id="a1",
            container_id="c1",
            pod_uid="pod-a:uid1",
            interface="eth0",
            generation=1,
        )

        self.assertEqual(first.address, replay.address)
        self.assertTrue(state.delete("a1"))
        self.assertTrue(state.delete("a1"))

    def test_partial_add_gc(self) -> None:
        state = CNIState("10.244.1.0/29")
        with self.assertRaises(RuntimeError):
            state.add(
                network="atlas",
                attachment_id="stale",
                container_id="c0",
                pod_uid="old:uid",
                interface="eth0",
                generation=1,
                fail_after_allocate=True,
            )

        # A partial inactive record must not permanently consume capacity.
        live = state.add(
            network="atlas",
            attachment_id="live",
            container_id="c1",
            pod_uid="new:uid",
            interface="eth0",
            generation=2,
        )
        self.assertTrue(live.active)

    def test_gc_generation(self) -> None:
        state = CNIState("10.244.1.0/29")
        state.add(
            network="atlas",
            attachment_id="a",
            container_id="c",
            pod_uid="pod:old",
            interface="eth0",
            generation=1,
        )
        state.add(
            network="atlas",
            attachment_id="b",
            container_id="c2",
            pod_uid="pod:new",
            interface="eth0",
            generation=2,
        )

        removed = state.gc({("b", 2)})

        self.assertEqual(removed, ["a"])
        self.assertTrue(state.check("b"))

    def test_status(self) -> None:
        state = CNIState("10.244.1.0/29")
        self.assertTrue(state.status({"ipam": True, "routes": True}))
        self.assertFalse(state.status({"ipam": True, "routes": False}))


if __name__ == "__main__":
    unittest.main()
