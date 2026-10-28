# Exercises — Module Design

## 1. Root-only responsibilities

What belongs in a root module that should not belong in a reusable child module?

## 2. Thin wrappers

Why is a one-resource wrapper often worse than using the provider resource directly?

## 3. Network responsibility

Define the responsibility and invariants of an `atlas_network` module.

## 4. Structured maps

Why are structured maps usually safer than parallel lists for subnet inputs?

## 5. Unsafe delegated input

Give an example of an input that improperly delegates a security decision to the caller.

## 6. Output leak

What makes an output an implementation leak?

## 7. Provider blocks

Why must reusable modules avoid provider configuration blocks?

## 8. Dependency inversion

Explain dependency inversion in module composition.

## 9. Confused ownership switches

Why can `create_x`/`existing_x_id` switches signal a confused ownership model?

## 10. Change classification

Classify these changes: add optional output; change default NAT profile; rename resource address; narrow input validation.

## 11. Move retention

How should `moved` blocks be maintained across module releases?

## 12. Proof levels

Design four proof levels for a network module.
