from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True, slots=True)
class StudyRoute:
    """One course-first learning route followed by an application transfer."""

    module: int
    slug: str
    stage: str
    question: str
    course_command: str
    focused_test_command: str
    capstone_command: str
    preserved_contract: str
    exit_evidence: str

    def evidence(self) -> dict[str, object]:
        return asdict(self)


STUDY_ROUTES = (
    StudyRoute(
        module=1,
        slug="runtime-objects-object-model",
        stage="observation",
        question="What objects and relationships exist at runtime?",
        course_command="make lab",
        focused_test_command="make lab-test",
        capstone_command="make capstone-manifest",
        preserved_contract="ordinary Python object identity remains the starting point",
        exit_evidence="explain function, class, module, and instance identities",
    ),
    StudyRoute(
        module=2,
        slug="runtime-observation-inspection",
        stage="observation",
        question="Which inspection routes observe without accidental execution?",
        course_command="make observation-lab",
        focused_test_command="make observation-lab-test",
        capstone_command="make capstone-manifest",
        preserved_contract="Module 01 object identities remain distinguishable",
        exit_evidence="classify visible names, stored state, and resolved values",
    ),
    StudyRoute(
        module=3,
        slug="signatures-provenance-runtime-evidence",
        stage="observation",
        question="Which runtime evidence is strong enough to support a claim?",
        course_command="make evidence-lab",
        focused_test_command="make evidence-lab-test",
        capstone_command="make capstone-bind-action",
        preserved_contract="observation remains separate from execution",
        exit_evidence="bind a call and label provenance limits without invoking it",
    ),
    StudyRoute(
        module=4,
        slug="function-wrappers-transparent-decorators",
        stage="callable control",
        question="What must a wrapper preserve to remain honest?",
        course_command="make wrapper-lab",
        focused_test_command="make wrapper-lab-test",
        capstone_command="make capstone-action-wrapper",
        preserved_contract="runtime evidence still reaches the original callable",
        exit_evidence="trace definition, application, binding, and call-time ownership",
    ),
    StudyRoute(
        module=5,
        slug="decorator-design-policies-typing",
        stage="callable control",
        question="Which policies belong at a callable boundary?",
        course_command="make decorator-policy-lab",
        focused_test_command="make decorator-policy-lab-test",
        capstone_command="make capstone-check-action",
        preserved_contract="wrapper signatures and failure identity remain visible",
        exit_evidence="bound retry, validation, and cache claims to explicit policy",
    ),
    StudyRoute(
        module=6,
        slug="class-customization-pre-metaclasses",
        stage="class control",
        question="Can a lower-power class tool own the behavior?",
        course_command="make class-customization-lab",
        focused_test_command="make class-customization-lab-test",
        capstone_command="make capstone-class-creation",
        preserved_contract="callable policy remains outside class-wide machinery",
        exit_evidence="compare helper, property, descriptor, decorator, and metaclass scope",
    ),
    StudyRoute(
        module=7,
        slug="descriptors-lookup-attribute-control",
        stage="attribute control",
        question="Which lookup layer owns this attribute result?",
        course_command="make descriptor-lookup-lab",
        focused_test_command="make descriptor-lookup-lab-test",
        capstone_command="make capstone-field-ownership",
        preserved_contract="class customization does not obscure ordinary lookup",
        exit_evidence="predict precedence, binding, and per-instance storage",
    ),
    StudyRoute(
        module=8,
        slug="descriptor-systems-validation-framework-design",
        stage="attribute control",
        question="Which field-system powers have earned their complexity?",
        course_command="make descriptor-system-lab",
        focused_test_command="make descriptor-system-lab-test",
        capstone_command="make capstone-field-system",
        preserved_contract="one-field lookup and storage ownership remain explicit",
        exit_evidence="place cache, storage, composition, and hint policy boundaries",
    ),
    StudyRoute(
        module=9,
        slug="metaclass-design-class-creation",
        stage="class creation",
        question="What must happen before the class exists?",
        course_command="make class-creation-lab",
        focused_test_command="make class-creation-lab-test",
        capstone_command="make capstone-class-creation",
        preserved_contract="lower-power attribute and class tools remain preferred",
        exit_evidence="trace namespace, hook, registry, and metaclass ownership",
    ),
    StudyRoute(
        module=10,
        slug="runtime-governance-mastery-review",
        stage="governance",
        question="Which runtime powers should be approved, constrained, or rejected?",
        course_command="make runtime-governance-lab",
        focused_test_command="make runtime-governance-lab-test",
        capstone_command="make capstone-governance",
        preserved_contract="mechanisms remain observable and no more powerful than required",
        exit_evidence="publish a decision with owner, rollback, proof, and escalation boundary",
    ),
)


def route_for(module: int) -> StudyRoute:
    """Return the stable study route for one substantive module."""

    for route in STUDY_ROUTES:
        if route.module == module:
            return route
    raise ValueError("module must be between 1 and 10")
