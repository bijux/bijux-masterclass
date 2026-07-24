"""Module 04: tree-safe recursion tools (end-of-Module-09).

Public surface:
- Stack-safe preorder traversal (`flatten`, `iter_flatten_buffered`)
- Safe folds/scans (`fold_tree_buffered`, `scan_tree`, ...)

`TreeDoc` and `TextNode` live in `funcpipe_rag.core.rag_types`.
"""

from __future__ import annotations

from ._traversal import (
    Path,
    assert_acyclic,
    flatten,
    flatten_via_fold,
    iter_flatten,
    iter_flatten_buffered,
    max_depth,
    recursive_flatten,
)
from .folds import (
    fold_count_length_maxdepth,
    fold_tree,
    fold_tree_buffered,
    fold_tree_no_path,
    linear_accumulate,
    linear_reduce,
    scan_count_length_maxdepth,
    scan_tree,
)

__all__ = [
    "Path",
    "assert_acyclic",
    "flatten",
    "flatten_via_fold",
    "fold_count_length_maxdepth",
    "fold_tree",
    "fold_tree_buffered",
    "fold_tree_no_path",
    "iter_flatten",
    "iter_flatten_buffered",
    "linear_accumulate",
    "linear_reduce",
    "max_depth",
    "recursive_flatten",
    "scan_count_length_maxdepth",
    "scan_tree",
]
