# Course 5 predecessor handoff

Course 6 consumes the exact ten-file Course 5 handoff under `capstone/predecessor/handoff/`. It inherits service names, DNS contracts, Gateway authority, network-policy expectations, topology assumptions, and egress restrictions.

The handoff explicitly does **not** claim storage durability, CSI correctness, snapshot validity, backup integrity, or restore success. Those become Course 6 responsibilities.
