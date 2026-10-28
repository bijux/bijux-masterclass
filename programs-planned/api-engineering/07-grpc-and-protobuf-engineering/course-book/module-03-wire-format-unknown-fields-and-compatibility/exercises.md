# Exercises — Module 03: Wire Format, Unknown Fields, and Compatibility Discipline

Work through all twelve problems before opening the answers. In **Wire Format, Unknown Fields, and Compatibility Discipline**, every response must settle this question: **How can an RPC contract evolve without corrupting old data, breaking generated clients, or creating behavior that is wire-readable but operationally unsafe?** Do not stop at terminology. Show how the decision changes a request, durable state, consumer, operator action, or release result, and state how that consequence is tested.

## 1. Why is reusing a removed field number more dangerous than reusing a local variable name?

Write a concise engineering answer and name the decisive proof.

## 2. Classify renaming a field while keeping its tag across four compatibility dimensions.

Write a concise engineering answer and name the decisive proof.

## 3. Why is `int32` to `sint32` unsafe despite both representing integers?

Write a concise engineering answer and name the decisive proof.

## 4. When may an old intermediary safely drop unknown fields?

Write a concise engineering answer and name the decisive proof.

## 5. Classify adding a new enum value for a TypeScript consumer with an exhaustive switch.

Write a concise engineering answer and name the decisive proof.

## 6. Why should changing unary `GetRun` to server-streaming create a new method?

Write a concise engineering answer and name the decisive proof.

## 7. What must be reserved when a published field is removed?

Write a concise engineering answer and name the decisive proof.

## 8. Compare a golden binary fixture with a descriptor set.

Write a concise engineering answer and name the decisive proof.

## 9. Why can a string-to-bytes change be wire-readable but still breaking?

Write a concise engineering answer and name the decisive proof.

## 10. What does Buf breaking analysis prove, and what does it not prove?

Write a concise engineering answer and name the decisive proof.

## 11. Why is creating a v2 package not a substitute for migration planning?

Write a concise engineering answer and name the decisive proof.

## 12. Define a release gate for an additive optional response field.

Write a concise engineering answer and name the decisive proof.
