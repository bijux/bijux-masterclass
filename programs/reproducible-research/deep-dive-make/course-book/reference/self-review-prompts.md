# Self-Review Prompts

Use this page when you want short prompts that turn Make concepts into active review
judgment instead of command memorization.

## Graph truth

- Which edge explains this rebuild honestly?
- What would prove convergence here instead of only one successful run?
- Which change would make this build lie even if it still "works" once?

## Public contract and artifacts

- Which target is truly public, and which one are you only assuming is public?
- Which output is a build result, which is proof evidence, and which is only controlled example material?
- What would another maintainer inspect first before trusting this build?

## Incidents and stewardship

- Which command gives the cheapest clarifying evidence for this incident?
- Which failure class would you suspect first if serial works and `-j` breaks?
- Which architectural layer would you inspect before approving the next non-trivial change?

## Public target prompts

- Which target should another reviewer trust first without reading recipes?
- What does `selftest` prove that `all` does not?
- Which output is meant to be consumed directly and which is only review evidence?
