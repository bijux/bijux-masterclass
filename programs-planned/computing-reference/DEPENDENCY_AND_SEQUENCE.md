# Dependency and Sequence

## Five coherent families

### A. Programming-language family

1. Programming Languages & Semantics
2. Object-Oriented Programming
3. Functional Programming
4. Concurrent & Parallel Programming
5. Systems Programming
6. Metaprogramming
7. Theory of Programming
8. Compilers & Language Implementation

Program 01 is the semantic spine. Programs 02–06 apply or deepen distinct programming models. Program 07 provides the formal theory. Program 08 realizes languages as toolchains and runtimes.

### B. Software-engineering family

9. Software Design & Domain Modeling
10. Methods & Evolution
11. Patterns
12. Software Architecture
13. Testing & Quality Engineering
14. Software Delivery & Reliability Engineering

Program 09 owns code and domain structure. Program 11 owns recurring solution forms. Program 12 owns system-wide structure. Program 10 owns lifecycle and organizational method. Program 13 owns evidence about quality. Program 14 owns safe delivery and production reliability.

### C. Computational foundations

15. Theory of Computation & Complexity
16. Algorithm Engineering
17. Data Structures Engineering

Program 15 owns what is computable and efficiently computable. Program 16 owns algorithm design, proof, implementation, and experiment. Program 17 owns representation and operation invariants.

### D. Data family

18. Database Engineering
19. Data Engineering
20. Data Architecture Engineering
21. Large-Scale Data Systems Engineering

Program 18 owns database engines and transactional data. Program 19 owns pipelines and data products. Program 20 owns organization-wide structure, ownership, semantics, and governance. Program 21 owns distributed data-engine internals and extreme scale.

### E. Systems and infrastructure family

22. Operating Systems
23. Computer Architecture
24. Network Engineering
25. Security Engineering
26. Systems Engineering
27. Distributed Systems Engineering
28. API & Service Engineering
29. Platform Engineering
30. Cloud & Infrastructure Engineering

These move from machine and kernel foundations through communication, trust, whole-system engineering, distributed coordination, service interfaces, internal platforms, and cloud infrastructure.

## Recommended foundation spine

A learner may study several programs in parallel, but these dependencies should be respected:

```text
Programming Languages & Semantics
    ├── OOP / FP / Metaprogramming / Compilers
    └── Systems Programming
             ├── Operating Systems
             └── Network Engineering

Data Structures ──┬── Algorithm Engineering
                  ├── Database Engineering
                  └── Distributed Systems

Computer Architecture
    ├── Systems Programming
    ├── Operating Systems
    └── Concurrent & Parallel Programming

Software Design
    ├── Patterns
    ├── Architecture
    ├── Testing
    └── API & Service Engineering

Networking + Operating Systems + Databases
    └── Distributed Systems
            ├── Large-Scale Data Systems
            ├── API & Service Engineering
            ├── Platform Engineering
            └── Cloud & Infrastructure Engineering
```

## Horizontal production order

When authoring the corpus, use horizontal waves:

1. author Module 001 for all 30 programs;
2. then Module 002 for all 30;
3. continue through Module 050;
4. audit all Level-I programs;
5. continue Modules 051–100 in the same way.

This keeps the whole canon calibrated and prevents one program from becoming polished while the rest remain speculative.

The production order does not imply that a learner must take all 30 programs simultaneously.
