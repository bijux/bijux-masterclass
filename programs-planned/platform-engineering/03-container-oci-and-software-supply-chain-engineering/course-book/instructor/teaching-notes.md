# Instructor delivery notes

The course should be taught from objects and failures, not a slide deck of container products.

## Before each module

- verify the lab’s privilege and cleanup boundaries;
- choose one artifact to trace live;
- prepare one planted defect;
- identify the strongest evidence available in the room;
- avoid promising native/cloud evidence when tools are absent.

## During explanation

Ask repeatedly:

```text
What object are we holding?
Who owns it?
What is its stable identity?
What transition changes it?
Which evidence would disprove the claim?
```

Do not answer every tool question immediately. Translate it to the underlying object or protocol first.

## Primary misconceptions

- image equals container;
- non-root equals safe;
- final rootfs proves no secret history;
- digest equals trustworthy;
- tag equals release;
- one platform test covers the index;
- SBOM equals vulnerability proof;
- signature equals authorization;
- reproducible equals secure;
- Kubernetes will fix runtime ambiguity.

## Review cadence

After Modules 3, 6, and 9, run cumulative design reviews. Require the learner to rebuild the evidence chain from source to release without notes.
