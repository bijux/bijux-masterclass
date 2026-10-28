# Program Evidence Ladder

Evidence is classified by the environment in which the mechanism was exercised. Static configuration checks, semantic unit tests, local host experiments, virtual-machine trials, and real-cloud observations answer different questions.

A successful local TLS fixture proves certificate parsing and hostname verification. It does not prove public DNS control, internet routing, managed-certificate renewal, or external load-balancer behavior. A cloud deployment proves those provider integrations only for the recorded region, account, configuration, and time.

Every course records executed, skipped, and environment-backed checks separately.
