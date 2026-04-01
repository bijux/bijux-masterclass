# Module 03: State and Typestate

State is where object-oriented systems usually become ambiguous. This module treats
state as something designed deliberately rather than accumulated incidentally.

## Main questions

- When is `@property` a clarity tool and when is it a trap?
- Which dataclass subsets are reliable and which combinations become brittle?
- How do you keep invalid states from leaking into the domain?
- How should `None`, partial objects, and lifecycle transitions be represented?
- How can Python APIs make illegal operations difficult without pretending to be a theorem prover?

## Outcome

You should finish this module able to model lifecycles, validation rules, and null
semantics with fewer hidden states and fewer ad hoc runtime checks.
