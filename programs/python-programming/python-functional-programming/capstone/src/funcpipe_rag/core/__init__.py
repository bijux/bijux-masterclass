"""Core helpers used across modules (rules, safety lint, streaming dedup).

End-of-Module-09 snapshot."""

from .rules_dsl import (
    abstract_min_len,
    any_doc,
    category_startswith,
    none_doc,
    parse_rule,
    rule_all,
    rule_and,
    rule_not,
    rule_or,
    title_contains,
)
from .rules_lint import SafeVisitor, assert_rule_is_safe_expr
from .rules_pred import (
    DEFAULT_RULES,
    All,
    AnyOf,
    Eq,
    LenGt,
    Not,
    Pred,
    RulesConfig,
    StartsWith,
    eval_pred,
)
from .structural_dedup import DedupIterator, structural_dedup_lazy

__all__ = [
    "DEFAULT_RULES",
    "All",
    "AnyOf",
    "DedupIterator",
    "Eq",
    "LenGt",
    "Not",
    "Pred",
    "RulesConfig",
    "SafeVisitor",
    "StartsWith",
    "abstract_min_len",
    "any_doc",
    "assert_rule_is_safe_expr",
    "category_startswith",
    "eval_pred",
    "none_doc",
    "parse_rule",
    "rule_all",
    "rule_and",
    "rule_not",
    "rule_or",
    "structural_dedup_lazy",
    "title_contains",
]
