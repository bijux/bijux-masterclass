from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping, Any


@dataclass(frozen=True)
class PlatformReleaseDecision:
    decision: str
    reasons: tuple[str,...]


def evaluate_platform_release(*, catalog_valid: bool, registry_valid: bool,
                              policy_decision: str, lifecycle_safe: bool,
                              template_safe: bool, docs_complete: bool,
                              sdk_traceable: bool, runtime_safe: bool,
                              sandbox_safe: bool) -> PlatformReleaseDecision:
    failures=[]
    for name,ok in [
        ("catalog",catalog_valid),("registry",registry_valid),("lifecycle",lifecycle_safe),
        ("template",template_safe),("documentation",docs_complete),("sdk",sdk_traceable),
        ("runtime",runtime_safe),("sandbox",sandbox_safe),
    ]:
        if not ok: failures.append(name)
    if policy_decision=="fail": failures.append("policy")
    if failures:
        return PlatformReleaseDecision("rejected",tuple(failures))
    if policy_decision=="review":
        return PlatformReleaseDecision("review",("approved-exception-or-human-judgment-required",))
    return PlatformReleaseDecision("accepted",())
