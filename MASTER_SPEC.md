# Master Specification

## 1. Governing intent

This is not a certificate catalogue, a list of fashionable tools, or a plan to consume more disconnected courses.

It is a structured reconstruction of computing and software-engineering knowledge for an experienced practitioner who has learned across programming, backend systems, data science, HPC, cloud, MLOps, research software, and production engineering.

The system must:

- take existing islands of knowledge;
- reveal and fill genuine gaps;
- update stale knowledge;
- connect concepts into one causal and coherent model;
- force retrieval, reasoning, implementation awareness, and teaching;
- remain useful as a durable reference;
- avoid filler, artificial quotas, and hidden workload explosions.

## 2. Canonical scope

The blueprint contains exactly:

- 30 programs;
- 2 mandatory levels per program;
- 50 modules per level;
- 100 modules per program;
- 3,000 planned modules in total.

No mandatory Level III is included in v1. See `LEVEL_III_POLICY.md`.

## 3. Meaning of a program

A program is a durable professional and academic domain that can justify sustained study throughout a career.

A program must have:

- a distinct governing problem;
- a recognizable body of theory and practice;
- a coherent progression from foundations to graduate/professional depth;
- real workplace responsibilities associated with the title;
- explicit boundaries against adjacent programs;
- enough substance for 100 non-filler modules;
- a path to future specialization without distorting the core.

## 4. Meaning of a level

### Level I — Modules 001–050

Level I is a rigorous undergraduate core. It assumes the learner is technically capable and does not waste time on empty motivational material.

It must establish:

- precise vocabulary;
- first-principles models;
- canonical mechanisms;
- foundational proofs or invariants where relevant;
- implementation awareness;
- basic failure and trade-off reasoning;
- competence comparable in rigor to a strong sequence of university subjects.

### Level II — Modules 051–100

Level II is graduate and professional depth.

It must add:

- advanced mechanisms and models;
- system internals;
- difficult edge cases;
- competing designs;
- pathological and adversarial behavior;
- production constraints;
- papers or authoritative specifications where appropriate;
- independent design and review judgment.

Level II must not merely repeat Level I with the word “advanced.”

## 5. Module granularity

Every module is one bounded, self-contained chapter.

The workload may increase gradually in intellectual independence, but it must not explode in volume.

A module must not hide:

- a semester project;
- a full compiler, database, operating system, or platform;
- a multi-week reading list;
- an undefined “research project”;
- a capstone;
- multiple unrelated topics joined to fill a quota.

Large constructions are decomposed across consecutive modules.

## 6. One-file rule

Every completed module will exist as exactly one Markdown file containing all required teaching material, worked examples, exercises, and answers.

No required content may be hidden in:

- a separate lab;
- a notebook;
- a slide deck;
- an answer key;
- an instructor guide;
- an external video;
- a generated image.

External sources support the chapter; they do not replace it.

## 7. Professional-readiness interpretation

Completing a program should provide the conceptual, technical, and evaluative knowledge expected from someone working in that domain.

It does not claim to replace:

- years of production responsibility;
- organizational leadership evidence;
- regulated professional certification;
- a university degree;
- research apprenticeship.

The content must nevertheless be concrete enough to prepare a serious learner for real design, implementation, review, diagnosis, and interview work.

## 8. Anti-filler rules

The following are prohibited as module titles or scopes:

- overview;
- advanced topics;
- miscellaneous topics;
- future directions;
- final synthesis;
- capstone;
- comprehensive project;
- tool survey without a governing concept;
- generic “best practices”;
- repetition owned by another program.

A concluding module is acceptable only when it names a precise object of analysis and adds a distinct mode of reasoning.

## 9. Tool policy

Tools may appear as implementations and case studies.

A tool may not become the conceptual owner of a module merely because it is popular.

For example:

- Kafka illustrates partitioned logs and consumer coordination;
- Spark illustrates cluster dataflow execution;
- Kubernetes illustrates reconciliation and workload orchestration;
- Terraform/OpenTofu illustrates declarative infrastructure;
- PostgreSQL illustrates relational storage, MVCC, and query planning.

The durable concept is taught first.

## 10. Change control

Roadmap changes require:

1. identification of a concrete omission, duplication, ordering error, or boundary violation;
2. an impact analysis across all affected programs;
3. manifest regeneration;
4. validation;
5. an atomic commit.

Do not rewrite a roadmap for cosmetic novelty.
