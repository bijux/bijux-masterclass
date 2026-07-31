"""Executable independent-study routes for the metaprogramming course."""

from .catalog import STUDY_ROUTES, StudyRoute, route_for
from .evidence import build_study_evidence, render_study_evidence
from .reentry import ReentryPlan, build_reentry_plan
from .transfer import (
    CAPSTONE_TRANSFERS,
    CapstoneTransfer,
    transfer_for,
    transfer_target_evidence,
)

__all__ = [
    "STUDY_ROUTES",
    "CAPSTONE_TRANSFERS",
    "CapstoneTransfer",
    "ReentryPlan",
    "StudyRoute",
    "build_reentry_plan",
    "build_study_evidence",
    "render_study_evidence",
    "route_for",
    "transfer_for",
    "transfer_target_evidence",
]
