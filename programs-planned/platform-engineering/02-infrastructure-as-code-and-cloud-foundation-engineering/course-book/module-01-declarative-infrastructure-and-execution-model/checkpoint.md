# Checkpoint — Declarative Execution and Plan Review

## Required evidence

Retain:

- one accepted semantic plan with explained actions;
- one policy-rejected plan;
- state lineage/serial and saved-plan identity;
- stale-serial and wrong-lineage rejections;
- the unstable-key failure and corrected semantic-key design;
- proposed move mappings for existing objects;
- provider/OpenTofu dependency identity;
- a post-apply data-plane validation list.

## Decision defense

Explain configuration, state, provider model, remote control plane, and data plane as separate representations. For every plan action, identify whether its cause is intent, address identity, provider behavior, refresh, or policy. State which race a saved plan reduces and which environmental races remain.

## Progression gate

You pass only when another reviewer can reconstruct why each action exists and what observation would prove the resulting platform. A plan summary, green syntax check, or zero-destroy count is not sufficient evidence.
