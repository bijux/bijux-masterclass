# Command Outcome Matrix

## The product

Build a command dispatcher where the selected command determines the return type. The command union should include at least:

- a command with a literal result;
- a command with a scalar result;
- a command with a discriminated success/failure result.

The central relationship is:

```text
command discriminant → selected command member → outcome type → runtime branch
```

Read [Module 23](../../course-book/module-23-conditional-types-infer-and-type-level-control-flow/index.md) before implementation.

## Public contract

Define `Command`, `Outcome<C>`, and `execute<C extends Command>(command: C): Outcome<C>`. A `ping` call should infer `'pong'`; a length command should infer `number`; division should infer a result union that represents division by zero without throwing.

The runtime switch must be exhaustive over the same discriminant used by the conditional type. The public signature may not use a caller-selected free result parameter such as `execute<T>(command): T`.

## Milestones

1. Write the command-to-outcome table in prose before writing a conditional type.
2. Implement one conditional branch at a time and test it with named type aliases.
3. Prove distribution behavior over the command union.
4. Implement exhaustive runtime dispatch.
5. Localize any generic-return assertion to the dispatcher and state its switch invariant.
6. Add positive and rejected type tests for each command.
7. Add runtime tests for all terminal outcomes.
8. Inspect the emitted declaration and simplify unreadable conditional expressions with named aliases.

## Adversarial cases

Add a new command and observe both compiler and runtime exhaustiveness failures. Test a union-typed command variable and explain why its result becomes a union. Attempt to return a value from the wrong branch and identify whether the checker catches it directly or only after a local assertion boundary.

Also test unsupported external JSON. A type assertion to `Command` must not be accepted as runtime parsing.

## Design record

Record:

- where conditional distribution is useful;
- where tuple wrapping would be required to treat a union as one value;
- what `never` means in the final branch;
- why `infer` extracts relationships but cannot establish runtime command validity;
- whether adding a command is compatible for producers, dispatchers, and exhaustive consumers.

## Independent transfer

Rebuild the pattern for request/response messages, AST nodes, or database operations. Include one generic command whose output is extracted from a witness carried by the command.

## Completion standard

The same discriminant table must explain the conditional type, runtime switch, tests, declaration, and compatibility note. If any layer uses an independent handwritten mapping, the lab is incomplete.
