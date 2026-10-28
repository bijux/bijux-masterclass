# Laboratory 2 — Usage Quote Policy

## Product and purpose

This quotation engine makes JavaScript coercion visible in a domain where zero is valid and money must remain integral. Its purpose is not realistic billing complexity; it is exact acceptance, conversion, policy lookup, and deterministic representation.

## Entry standard

Write the acceptance–conversion–domain table for plan names, unit text, safe integer range, and cents before opening the implementation. Predict the Module 2 cases, especially zero, truthiness, `NaN`, indexed absence, and operand-returning logical operators. The starter confirms the package route and one simple policy lookup; it does not establish the accepted input language or billing invariant.

## Public contract

Plans are starter, team, and enterprise. Units are canonical decimal digits, 0–1,000,000. Starter includes 100 and charges five cents per extra unit; team includes 1,000 and charges two cents; enterprise charges zero. The quote records raw policy consequences rather than only a formatted total.

## Required construction sequence

Write the exact unit parser first. Add the closed plan predicate and policy table, then derive included, billable, and total cents. Keep currency rendering separate and use integer cents. Test zero, boundaries, exponent notation, signs, fractions, whitespace, unsupported plan, and values beyond the safe product range.

Keep the public surface small. Add private helpers only when they name a real step or invariant. Each exported function needs at least one success test and one boundary or failure test.

## Adversarial review

Exercise zero, included-limit boundaries, first billable unit, maximum units, one above maximum, exponent notation, signs, decimal points, surrounding whitespace, unknown plans, and arithmetic near the safe-integer limit. Verify that enterprise zero charges remain valid data and that duplicate or fallback plan logic cannot silently select another policy.

## Prohibited shortcuts

Do not use `parseInt`, loose equality, truthiness defaults, floating-point dollars, or a fallback plan. Do not treat zero total as absence. Do not scatter plan arithmetic through conditionals when one table can own it.

A shortcut is prohibited because it destroys the reasoning target, not because the reference implementation uses a different style.

## Completion evidence

The laboratory is complete when the accepted unit language is written and tested, every plan policy has boundary evidence, all money remains integer cents, zero is preserved as a valid result, and rendering is separate from calculation. Demonstrate that exponent, signed, fractional, whitespace, and out-of-range inputs fail for the intended reason, then compare policy representation—not line count—with the reference.

## Independent transfer

Add a trial plan that accepts only 0–25 units and rejects larger usage rather than calculating overage. Explain why this is a different policy shape from starter and team.

Write the trial plan’s acceptance and rejection table first. Identify the policy representation that can express “reject above 25” without pretending it is an overage rate, then add static exhaustiveness and boundary tests.
