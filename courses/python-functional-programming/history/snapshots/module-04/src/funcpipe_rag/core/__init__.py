"""Core helpers used across modules (rules, safety lint, streaming dedup)."""

from .rules_pred import (
    Pred,
    Eq,
    LenGt,
    StartsWith,
    All,
    AnyOf,
    Not,
    RulesConfig,
    DEFAULT_RULES,
    eval_pred,
)
from .rules_dsl import (
    any_doc,
    none_doc,
    category_startswith,
    title_contains,
    abstract_min_len,
    rule_and,
    rule_or,
    rule_not,
    rule_all,
    parse_rule,
)
from .rules_lint import SafeVisitor, assert_rule_is_safe_expr
from .structural_dedup import DedupIterator, structural_dedup_lazy

__all__ = [
    "Pred",
    "Eq",
    "LenGt",
    "StartsWith",
    "All",
    "AnyOf",
    "Not",
    "RulesConfig",
    "DEFAULT_RULES",
    "eval_pred",
    "any_doc",
    "none_doc",
    "category_startswith",
    "title_contains",
    "abstract_min_len",
    "rule_and",
    "rule_or",
    "rule_not",
    "rule_all",
    "parse_rule",
    "SafeVisitor",
    "assert_rule_is_safe_expr",
    "DedupIterator",
    "structural_dedup_lazy",
]
