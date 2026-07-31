from __future__ import annotations

from dataclasses import asdict, dataclass

from .catalog import StudyRoute, route_for


@dataclass(frozen=True, slots=True)
class ReentryPlan:
    """A bounded return route based on the last contract a learner still trusts."""

    last_trusted_module: int
    refresh: StudyRoute | None
    continue_with: StudyRoute
    order: tuple[str, ...]
    broad_gate_deferred: bool = True

    def evidence(self) -> dict[str, object]:
        packet = asdict(self)
        packet["refresh"] = None if self.refresh is None else self.refresh.evidence()
        packet["continue_with"] = self.continue_with.evidence()
        return packet


def build_reentry_plan(last_trusted_module: int) -> ReentryPlan:
    """Build a course-first plan without pretending memory is executable proof."""

    if not 0 <= last_trusted_module <= 10:
        raise ValueError("last trusted module must be between 0 and 10")

    if last_trusted_module == 0:
        first = route_for(1)
        return ReentryPlan(
            last_trusted_module=0,
            refresh=None,
            continue_with=first,
            order=(
                "read the Module 00 study contract",
                first.course_command,
                first.focused_test_command,
                first.capstone_command,
            ),
        )

    refresh = route_for(last_trusted_module)
    continuation = route_for(min(last_trusted_module + 1, 10))
    return ReentryPlan(
        last_trusted_module=last_trusted_module,
        refresh=refresh,
        continue_with=continuation,
        order=(
            f"restate: {refresh.exit_evidence}",
            refresh.course_command,
            refresh.focused_test_command,
            continuation.course_command,
            continuation.focused_test_command,
            continuation.capstone_command,
        ),
    )
