# Governance Rules for Long-Lived Repositories

Good governance is not a thick policy document.

For this course, governance means small durable rules that protect state contracts after
the original maintainers move on.

## Write rules around high-risk changes

Useful governance rules often cover:

- new DVC-tracked data
- parameter changes with metric impact
- pipeline graph changes
- experiment promotion
- release bundle changes
- remote and retention changes
- recovery route changes

Example:

> Any pull request changing `dvc.yaml`, `dvc.lock`, `params.yaml`, or `publish/` must run
> the relevant verification route and explain the state contract being changed.

That rule is specific enough to review.

## Keep governance close to the work

Rules should live where maintainers will see them:

- review guide
- release guide
- recovery guide
- pull request template
- Makefile command names
- CI status checks

Governance hidden in a forgotten document does not protect the repository.

## Rules should teach what they protect

Weak:

> Follow DVC best practices.

Stronger:

> Do not merge DVC metadata changes unless the required remote objects are available to CI
> and another maintainer can restore the state from a clean checkout.

The stronger rule names the contract: shared recoverability.

## Governance should stay small

If every change requires the same heavy ritual, people will bypass the rules.

Use different review depth for different risk:

| Change | Reasonable rule |
| --- | --- |
| typo in documentation | normal review |
| parameter affecting metrics | params and metrics review |
| release bundle change | release audit route |
| remote migration | recovery and rollback plan |
| retention cleanup | dry run and approval |

Small rules survive longer.

## Review checkpoint

You understand this core when you can:

- write a rule for a high-risk state change
- place governance where maintainers will use it
- explain which contract a rule protects
- keep rules proportional to risk
- turn repeated review comments into durable guidance

Governance is successful when it makes the right action easier to repeat.
