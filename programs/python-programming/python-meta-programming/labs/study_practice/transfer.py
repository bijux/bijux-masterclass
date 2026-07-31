from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True, slots=True)
class CapstoneTransfer:
    """One course claim transferred into an observational application route."""

    module: int
    course_claim: str
    root_command: str
    course_command: str
    capstone_command: str
    owner: str
    question: str
    proves: str
    does_not_prove: str
    constructs_plugin: bool = False
    invokes_action: bool = False

    def evidence(self) -> dict[str, object]:
        return asdict(self)


CAPSTONE_TRANSFERS = (
    CapstoneTransfer(
        module=1,
        course_claim="runtime objects expose stable public relationships",
        root_command="capstone-manifest",
        course_command="capstone-manifest",
        capstone_command="manifest",
        owner="framework.py manifest helpers",
        question="Which plugin classes, fields, and actions exist on the public surface?",
        proves="the imported runtime publishes deterministic structural metadata",
        does_not_prove="that constructing a plugin or invoking an action succeeds",
    ),
    CapstoneTransfer(
        module=2,
        course_claim="observation must stay separate from application execution",
        root_command="capstone-manifest",
        course_command="capstone-manifest",
        capstone_command="manifest",
        owner="framework.py manifest helpers and cli.py",
        question="Which runtime facts can be exported without plugin invocation?",
        proves="manifest inspection does not invoke plugin actions",
        does_not_prove="that every possible attribute inspection is passive",
    ),
    CapstoneTransfer(
        module=3,
        course_claim="signature binding can validate call shape without invocation",
        root_command="capstone-bind-action",
        course_command="capstone-bind-action",
        capstone_command="bind-action",
        owner="framework.py action binding helper",
        question="Do proposed action arguments fit the stored callable signature?",
        proves="Python signature rules accept the proposed argument shape",
        does_not_prove="runtime hint compatibility, configuration validity, or action success",
    ),
    CapstoneTransfer(
        module=4,
        course_claim="wrapper transformations must preserve observable ownership",
        root_command="capstone-action-wrapper",
        course_command="capstone-action-wrapper",
        capstone_command="action-wrapper",
        owner="actions.py and framework.py wrapper inspection",
        question="Which layer owns ActionSpec, __signature__, and __wrapped__?",
        proves="the wrapper chain preserves explicit metadata and provenance",
        does_not_prove="that invoking the wrapped action succeeds",
    ),
    CapstoneTransfer(
        module=5,
        course_claim="runtime policy must state its supported contract and refusals",
        root_command="capstone-check-action",
        course_command="capstone-check-action",
        capstone_command="check-action",
        owner="actions.py hint policy and framework.py binding",
        question="Which bound values match the deliberately supported runtime hints?",
        proves="supported hints are checked and unsupported hints are reported",
        does_not_prove="a complete Python runtime type system or successful invocation",
    ),
    CapstoneTransfer(
        module=6,
        course_claim="lower-power class tools must be considered before metaclasses",
        root_command="capstone-class-creation",
        course_command="capstone-class-creation",
        capstone_command="class-creation",
        owner="framework.py stored class-creation provenance",
        question="Which finished-class requirements would a lower-power tool still own?",
        proves="the report separates generated structure and registration owners",
        does_not_prove="that PluginMeta is automatically the best owner",
    ),
    CapstoneTransfer(
        module=7,
        course_claim="descriptor lookup and storage ownership must remain inspectable",
        root_command="capstone-field-ownership",
        course_command="capstone-field-ownership",
        capstone_command="field-ownership",
        owner="fields.py and framework.py field collection",
        question="Which descriptor owns endpoint lookup and where is its value stored?",
        proves="descriptor category, class access, collection, and storage are visible",
        does_not_prove="system-wide cache, external storage, or transaction semantics",
    ),
    CapstoneTransfer(
        module=8,
        course_claim="field-system powers must be accepted or rejected explicitly",
        root_command="capstone-field-system",
        course_command="capstone-field-system",
        capstone_command="field-system",
        owner="fields.py and framework.py collected field system",
        question="Which descriptor-system powers belong in this application?",
        proves="the capstone names accepted field owners and rejected wider powers",
        does_not_prove="a production ORM, cache, or external storage framework",
    ),
    CapstoneTransfer(
        module=9,
        course_claim="class-creation power must be justified by pre-class facts",
        root_command="capstone-class-creation",
        course_command="capstone-class-creation",
        capstone_command="class-creation",
        owner="framework.py PluginMeta",
        question="What required namespace preparation, shaping, and registration timing?",
        proves="stored provenance identifies each class-creation hook and output",
        does_not_prove="package discovery, I/O, or automatic metaclass conflict repair",
    ),
    CapstoneTransfer(
        module=10,
        course_claim="runtime powers require approve, constrain, or reject decisions",
        root_command="capstone-governance",
        course_command="capstone-governance",
        capstone_command="governance",
        owner="governance.py and named mechanism owners",
        question="Which powers earned their cost and which remain outside the application?",
        proves="decisions name owners, observability, rollback, and proof routes",
        does_not_prove="the behavior of each mechanism without its focused report and tests",
    ),
)


def transfer_for(module: int) -> CapstoneTransfer:
    """Return the application transfer for one substantive course module."""

    for transfer in CAPSTONE_TRANSFERS:
        if transfer.module == module:
            return transfer
    raise ValueError("module must be between 1 and 10")
