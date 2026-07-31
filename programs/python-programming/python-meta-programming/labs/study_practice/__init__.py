"""Executable independent-study routes for the metaprogramming course."""

from .catalog import STUDY_ROUTES, StudyRoute, route_for
from .reentry import ReentryPlan, build_reentry_plan

__all__ = [
    "STUDY_ROUTES",
    "ReentryPlan",
    "StudyRoute",
    "build_reentry_plan",
    "route_for",
]
