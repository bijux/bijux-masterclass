# Roadmap Quality Gates

## Structural gates

A blueprint passes only if it contains:

- exactly 30 programs;
- exactly 10 blocks per program;
- exactly 10 modules per block;
- exactly 50 Level-I modules per program;
- exactly 50 Level-II modules per program;
- exactly 3,000 unique module IDs;
- exactly 3,000 unique module titles;
- exactly 3,000 unique future paths;
- continuous numbering from 001 through 100;
- no capstone or lab rows;
- no generated placeholder module files.

## Curriculum gates

Every program must pass all of the following.

### Distinct ownership

The program has a governing problem not owned more naturally by another program.

### Complete foundations

Level I contains the concepts that advanced material depends upon. It does not assume away the difficult foundations.

### Real graduate depth

Level II introduces advanced models, internals, failure, scale, formal reasoning, or professional judgment. It is not a renamed repeat of Level I.

### Coherent order

Every module has a reason to follow the previous material.

### Bounded grain

Every title describes a chapter-sized topic, not a semester project or a vague field.

### Tool independence

Tools appear as implementations of concepts, not substitutes for concepts.

### Work relevance

The roadmap supports actual design, implementation, review, debugging, operation, or research work associated with the program title.

### No quota padding

A module cannot exist merely to make the count reach 100.

## Automatic title rejection

The validator rejects exact or case-insensitive occurrences of:

- overview;
- advanced topics;
- miscellaneous;
- future directions;
- final synthesis;
- capstone;
- comprehensive project.

Human review must also reject euphemistic equivalents.

## Cross-program audit

Before changing a roadmap, check:

1. Does another program already own the concept?
2. Is the perspective genuinely different?
3. Are prerequisites explicit?
4. Does moving the topic create a gap elsewhere?
5. Is the new title precise enough to define one complete chapter?

## Content-production gates

A future module file does not count as complete merely because structural checks pass.

It also requires:

- professor-level conceptual review;
- hands-on engineering review;
- current-source verification;
- example and exercise review;
- code or mathematical validation where relevant;
- copy-editing for clarity and precision.
