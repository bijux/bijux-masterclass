# Glossary

Module 05 is where many workflows either become durable software systems or collapse into
unreviewable glue. This glossary helps you say which layer owns orchestration, which
layer owns implementation, and which layer owns runtime trust.

The aim is not impressive vocabulary. The aim is to make software-boundary decisions easy
to explain and defend.

## When to stop and check the glossary

Pause and check a term when:

- your explanation depends on "the code" without saying which layer owns it
- you are treating workflow scripts and reusable package code as if they were the same thing
- you can tell a rebuild matters but cannot yet name which software surface drifted
- you are using runtime, provenance, and environment as if they were interchangeable

## Terms

| Term | Meaning in this module |
| --- | --- |
| file contract | The visible rule-level declaration of meaningful inputs, outputs, params, and execution boundaries. |
| software boundary | The line between workflow orchestration and the software surfaces that implement behavior. |
| step-local code | Code owned by one workflow step, often a good fit for `workflow/scripts/`. |
| reusable package code | Logic under `src/` that deserves imports, tests, and reuse across steps. |
| runtime contract | The declared software environment or container boundary that gives a step stable execution meaning. |
| repository environment | A project-level software baseline for contributors and whole-repository workflow execution. |
| rule-scoped environment | A smaller runtime declaration attached to one rule or a small group of rules. |
| container boundary | A stronger machine-level execution surface used when host differences matter materially. |
| wrapper | A reusable command surface around an external tool that should reduce repeated plumbing without hiding meaning. |
| hidden dependency | A meaningful file or runtime requirement used by the implementation but not visible in the rule contract. |
| provenance artifact | A recorded file that travels with outputs and explains the software context of a run. |
| software drift | A change in helper code, runtime, or tool behavior that can invalidate output trust even when input files do not change. |
| rebuild evidence | The combination of rerun results and recorded software context that lets a reviewer trust new outputs. |
| publication trust | The degree to which released artifacts can still be defended after the run has finished. |
| ownership boundary | The answer to who owns orchestration, implementation, runtime, and review explanation for a workflow step. |

## How to use these terms

If a workflow change becomes hard to review, ask which term has become vague:

- is the file contract incomplete?
- is the software boundary unclear?
- is the runtime contract missing?
- is the provenance artifact too weak?

That habit keeps the module practical.

## Confusion pairs worth fixing early

These pairs matter because they decide where code belongs and how a reviewer should trust
it:

- `step-local code` versus `reusable package code`: step-local code serves one workflow
  step; reusable package code deserves imports, tests, and ownership beyond one rule.
- `repository environment` versus `rule-scoped environment`: the repository environment is
  the project baseline; a rule-scoped environment narrows runtime requirements for one
  step or one rule family.
- `runtime contract` versus `provenance artifact`: the runtime contract declares what a
  step needs to run; a provenance artifact records what actually produced the outputs.
- `hidden dependency` versus `software drift`: the hidden dependency is the missing
  declared influence; software drift is the trust problem that appears when code or
  runtime changes over time.

## Quick self-check

Before you leave Module 05, make sure you can answer these in a full sentence:

- If one Python helper is used by five rules and needs direct unit tests, which ownership
  surface should probably hold it?
- If a rule relies on a reference file or helper binary that never appears in its declared
  inputs or runtime boundary, what exact problem are you naming?
- If outputs changed after a package update even though input files stayed the same, which
  module term explains why reviewers should still care?
- If a release bundle includes the software context that produced it, which evidence
  artifact inside this module is doing that trust work?

## Terms you should be able to use by the end of the day

If Module 05 is landing properly, these terms should feel ordinary by the end:

- file contract
- step-local code
- reusable package code
- runtime contract
- hidden dependency
- software drift
- provenance artifact

If those still feel decorative rather than useful, revisit the worked example and the
first seven exercises before moving on.
