# Language and tool strategy

Kubernetes storage is expressed in several native forms:

- YAML for API objects and production-intent contracts;
- Python for transparent binders, CSI state machines, snapshot coordinators, backup catalogues, and proof orchestration;
- Go for a small filesystem durability probe close to the operating-system boundary;
- SQL and database concepts for transactional-state examples;
- shell and `kubectl` for optional cluster evidence.

The learner is not asked to implement a real CSI driver, database engine, or distributed filesystem. The semantic models are intentionally small enough to inspect completely. They exist to teach ownership and failure, not to substitute for native implementations.
