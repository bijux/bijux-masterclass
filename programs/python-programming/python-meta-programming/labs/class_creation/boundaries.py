from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True, slots=True)
class OwnershipDecision:
    """One reviewable decision about the smallest honest behavior owner."""

    pressure: str
    selected_owner: str
    reason: str
    refused_owner: str
    refusal_reason: str
    accepted_cost: str
    escalation_signal: str

    def manifest(self) -> dict[str, str]:
        return asdict(self)


DECISIONS = (
    OwnershipDecision(
        pressure="add one helper to one class",
        selected_owner="plain class definition",
        reason="the behavior is local and explicit",
        refused_owner="class decorator",
        refusal_reason="post-creation transformation adds no useful contract",
        accepted_cost="one ordinary method remains visible in the class body",
        escalation_signal="several unrelated classes need the same opt-in transformation",
    ),
    OwnershipDecision(
        pressure="validate one attribute on every assignment",
        selected_owner="descriptor",
        reason="the invariant belongs to attribute access",
        refused_owner="metaclass",
        refusal_reason="class creation is not the enforcement boundary",
        accepted_cost="descriptor lookup and per-instance storage must be documented",
        escalation_signal="the class family must also collect field declarations",
    ),
    OwnershipDecision(
        pressure="mark selected classes after creation",
        selected_owner="class decorator",
        reason="explicit post-creation opt-in preserves the needed timing",
        refused_owner="metaclass",
        refusal_reason="automatic hierarchy-wide policy is not required",
        accepted_cost="each participating class carries a visible decorator",
        escalation_signal="every future subclass must participate without opt-in",
    ),
    OwnershipDecision(
        pressure="register every concrete subclass in one class family",
        selected_owner="__init_subclass__",
        reason="the inherited hook already runs for each completed subclass",
        refused_owner="metaclass",
        refusal_reason="registration alone does not need namespace preparation or class shaping",
        accepted_cost="the base class owns an inherited creation-time side effect",
        escalation_signal="the rule needs assignment events before the subclass exists",
    ),
    OwnershipDecision(
        pressure="reject duplicate public names while a class body executes",
        selected_owner="metaclass __prepare__",
        reason="the duplicate event disappears from an ordinary final namespace",
        refused_owner="metaclass __new__",
        refusal_reason="the overwritten declaration cannot be reconstructed reliably",
        accepted_cost="a custom mapping participates in every class body",
        escalation_signal="the declaration language needs more than assignment tracking",
    ),
    OwnershipDecision(
        pressure="preserve tracked assignment events and build every plugin class contract",
        selected_owner="metaclass with external registry",
        reason="the family needs both a prepared namespace and automatic structural generation",
        refused_owner="__init_subclass__",
        refusal_reason="the completed subclass has already lost overwritten declaration events",
        accepted_cost="imports run class shaping and mutate resettable registry state",
        escalation_signal="plugins must be discovered across packages or processes",
    ),
    OwnershipDecision(
        pressure="discover installed plugins across processes",
        selected_owner="explicit discovery service",
        reason="deployment and environment state are outside class creation",
        refused_owner="metaclass",
        refusal_reason="a metaclass sees only classes imported in the current process",
        accepted_cost="discovery becomes an explicit I/O boundary",
        escalation_signal="discovery needs caching, versioning, or remote coordination",
    ),
)


def boundary_evidence() -> dict[str, object]:
    """Publish the owner ladder and costs used in Module 09 reviews."""

    return {
        "owner_ladder": [
            "plain class definition",
            "descriptor",
            "class decorator",
            "__init_subclass__",
            "metaclass",
            "explicit discovery service",
        ],
        "decisions": [decision.manifest() for decision in DECISIONS],
        "metaclass_acceptance_test": [
            "name the class-creation or automatic hierarchy-wide invariant",
            "show what the next-lower owner loses",
            "name import, inheritance, conflict, and reset costs",
            "keep runtime I/O and lifecycle orchestration outside the metaclass",
        ],
    }
