from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True, slots=True)
class GovernanceDecision:
    """One mechanism decision with the evidence required for approval."""

    pressure: str
    proposed_mechanism: str
    decision: str
    selected_owner: str
    lower_power_result: str
    blast_radius: str
    observability: str
    rollback: str
    proof: str
    escalation_signal: str

    def manifest(self) -> dict[str, str]:
        return asdict(self)


DECISIONS = (
    GovernanceDecision(
        pressure="evaluate adversarial tenant policy text",
        proposed_mechanism="eval with empty builtins",
        decision="reject",
        selected_owner="isolated policy service",
        lower_power_result="a bounded explicit policy model is preferred when sufficient",
        blast_radius="arbitrary code and resource use in the application process",
        observability="source and decisions need durable audit records",
        rollback="process termination, not Python namespace cleanup",
        proof="adversarial and resource-limit tests at the process boundary",
        escalation_signal="the policy language cannot remain declarative",
    ),
    GovernanceDecision(
        pressure="enforce action method signatures at runtime",
        proposed_mechanism="runtime-checkable Protocol",
        decision="reject",
        selected_owner="static type checker plus explicit call binding",
        lower_power_result="runtime protocol checks observe presence, not signatures",
        blast_radius="misleading runtime acceptance across every checked adapter",
        observability="signature inspection and binding reports",
        rollback="remove the overstated runtime check",
        proof="static type checks and executable binding failures",
        escalation_signal="values also require a published runtime validation subset",
    ),
    GovernanceDecision(
        pressure="replace one dependency during a focused test",
        proposed_mechanism="owner-local monkey patch",
        decision="constrain",
        selected_owner="scoped context-managed patch",
        lower_power_result="dependency injection remains preferred when the API permits it",
        blast_radius="other code can observe the replacement while active",
        observability="record owner, attribute, identities, and scope",
        rollback="finally restores or removes the exact attribute",
        proof="success, exception, and absent-attribute restoration tests",
        escalation_signal="parallel execution can observe shared mutable state",
    ),
    GovernanceDecision(
        pressure="serve one virtual module in a compiler test",
        proposed_mechanism="meta path finder",
        decision="constrain",
        selected_owner="exact-name context-managed tooling hook",
        lower_power_result="an explicit loader call is preferred outside import integration tests",
        blast_radius="process-wide import resolution while installed",
        observability="find, create, and execute events plus exact module name",
        rollback="remove finder and owned sys.modules entry",
        proof="installed, cleanup, ignored-name, and no-hook tests",
        escalation_signal="application behavior starts depending on the hook",
    ),
    GovernanceDecision(
        pressure="build plugin contracts from tracked class declarations",
        proposed_mechanism="PluginMeta",
        decision="approve",
        selected_owner="bounded class-family metaclass",
        lower_power_result="__init_subclass__ loses overwritten declaration events",
        blast_radius="class-family imports, inheritance, and metaclass composition",
        observability="non-constructing class-creation and registry reports",
        rollback="clear in-process registry; code changes remove generated policy",
        proof="namespace, class-creation, registry, field, and action tests",
        escalation_signal="discovery, reload, or external I/O enters class creation",
    ),
    GovernanceDecision(
        pressure="discover installed plugins during class creation",
        proposed_mechanism="metaclass package scanning",
        decision="reject",
        selected_owner="explicit discovery and configuration boundary",
        lower_power_result="the metaclass sees only classes already imported",
        blast_radius="filesystem or metadata I/O during import",
        observability="discovery manifest with source and enablement decisions",
        rollback="disable discovery independently from class definition",
        proof="adapter and discovery contract tests",
        escalation_signal="discovery spans processes or remote catalogs",
    ),
)


def selection_evidence() -> dict[str, object]:
    """Publish approval, constraint, and rejection decisions as data."""

    counts = {
        outcome: sum(decision.decision == outcome for decision in DECISIONS)
        for outcome in ("approve", "constrain", "reject")
    }
    return {
        "review_gate": [
            "name the pressure before the mechanism",
            "show what the lower-power owner loses",
            "bound blast radius and make behavior observable",
            "provide rollback and focused proof",
            "name the escalation signal and non-claims",
        ],
        "decisions": [decision.manifest() for decision in DECISIONS],
        "outcome_counts": counts,
    }
