from __future__ import annotations

import unittest

from scripts.doctor import CAP_NET_ADMIN, CAP_SYS_ADMIN, has_capability


class DoctorTests(unittest.TestCase):
    def test_capability_classification_uses_actual_bits(self) -> None:
        mask = (1 << CAP_NET_ADMIN)
        self.assertTrue(has_capability(mask, CAP_NET_ADMIN))
        self.assertFalse(has_capability(mask, CAP_SYS_ADMIN))
        self.assertFalse(has_capability(0, CAP_NET_ADMIN))


if __name__ == "__main__":
    unittest.main()
