# Instructor review questions

- Which immutable identities define this release?
- What exact objects will be created, changed, and deleted?
- Which fields and resources does the controller own?
- What would continue during repository or controller outage?
- Which evidence is structural, native, live-cluster, or operated?
- What is the rollback frontier?
- Who may authorize deletion of protected data?
- How does emergency state return to reviewed desired state?

## Extended reader notes

Useful review prompts include: Which identity is immutable here? What is the inventory boundary? Which fields are intentionally external? What happens when the source is unavailable? Which health rule observes current generation? How is a secret version adopted? What is the minimum canary population? Which data phase defines rollback? What prevents a generator from deleting unknown targets? Which Course 8 control will harden this authority?

Ask for one counterexample after every confident claim. For example, after “Synced means correct,” request a synchronized but wrong scenario. After “Git is the source of truth,” ask who owns the database row. Counterexamples expose abstraction leakage quickly.
