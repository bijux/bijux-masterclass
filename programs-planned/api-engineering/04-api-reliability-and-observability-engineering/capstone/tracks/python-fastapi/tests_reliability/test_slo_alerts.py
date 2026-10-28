from __future__ import annotations

import unittest

from api_reliability.alerts import BurnRateAlert, evaluate_burn_rate_alert
from api_reliability.slo import SLODefinition, SLOWindow, burn_rate


class SLOAlertTests(unittest.TestCase):
    def test_burn_rate(self) -> None:
        slo = SLODefinition("availability", 0.99, 28 * 24 * 3600)
        window = SLOWindow(good=970, total=1_000)
        self.assertAlmostEqual(burn_rate(slo, window) or 0, 3.0)

    def test_multiwindow_requires_both_windows(self) -> None:
        slo = SLODefinition("availability", 0.999, 28 * 24 * 3600)
        alert = BurnRateAlert("page-fast", "page", 3600, 300, 14.4, minimum_events=10)
        firing = evaluate_burn_rate_alert(
            slo,
            alert,
            long_window=SLOWindow(980, 1_000),
            short_window=SLOWindow(96, 100),
        )
        self.assertTrue(firing.firing)
        quiet = evaluate_burn_rate_alert(
            slo,
            alert,
            long_window=SLOWindow(980, 1_000),
            short_window=SLOWindow(100, 100),
        )
        self.assertFalse(quiet.firing)


if __name__ == "__main__":
    unittest.main()
