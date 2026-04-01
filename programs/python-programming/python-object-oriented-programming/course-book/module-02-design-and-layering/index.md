# Module 02: Design and Layering

Once the object model is clear, the next problem is assignment of responsibility.
This module moves from isolated objects to collaborating roles.

## Why this module matters

Many codebases become difficult not because individual objects are broken, but because
responsibilities are assigned arbitrarily. Work ends up split between "smart" entities,
"utility" modules, accidental god services, and inheritance trees that encode history
rather than design intent.

This module gives you criteria for deciding where behavior should live and how objects
should collaborate without turning the system into framework theater.

## Main questions

- Which responsibilities belong inside an object and which should move out?
- Why should composition be the default and inheritance the exception?
- When do semantic wrapper types improve correctness?
- How do duck typing, ABCs, and protocols fit different design pressures?
- How do you layer a Python system without turning it into framework theater?

## Reading path

1. Start with responsibilities, cohesion, and object smells.
2. Compare composition, inheritance, and semantic wrapper types before looking at layering.
3. Read interfaces and protocols after the role boundaries are clear.
4. Finish with the refactor chapter to see a thin layered design emerge from concrete pressure.

## Common failure modes

- placing behavior wherever the current developer happens to be editing
- reaching for inheritance to reuse code that should have been composed
- using raw strings and integers where domain meaning should be explicit
- creating a service layer so broad that it becomes a second god object
- introducing layers by directory naming alone without real boundary discipline

## Capstone connection

The capstone separates domain objects, evaluation policies, runtime orchestration,
repositories, and adapters on purpose. This module gives the reasoning for that split:
why `MonitoringPolicy` should not fetch metrics, why strategies should own evaluation
variability, and why the runtime facade should coordinate without absorbing domain logic.

## Outcome

You should finish this module able to decompose object-heavy code into explicit
roles with cleaner cohesion and more stable collaboration boundaries.
