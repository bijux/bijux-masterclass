from __future__ import annotations

from pprint import pprint

from .scenario import build_default_observation


def main() -> None:
    result = build_default_observation()

    print("Cycle report:")
    pprint(result.cycle_report)
    print("\nPolicy summary:")
    pprint(result.snapshot.summary)
    print("\nActive rule index:")
    pprint(result.snapshot.active_rule_index)
    print("\nOpen incidents:")
    pprint(result.snapshot.open_incidents)


if __name__ == "__main__":
    main()
