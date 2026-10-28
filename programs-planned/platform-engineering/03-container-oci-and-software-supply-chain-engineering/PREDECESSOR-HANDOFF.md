# Course 2 predecessor handoff

Course 3 consumes `capstone/predecessor/` byte-for-byte from Atlas Cloud Foundation 1.0.

The handoff fixes the following before image design begins:

- Atlas API listens on port 8080 behind a governed edge;
- API and worker use separate non-root identities;
- `/var/lib/atlas/spool` and `/var/lib/atlas/results` are durable state;
- `/run/atlas` is ephemeral;
- configuration and secrets are runtime inputs, not image content;
- the root filesystem is replaceable;
- shutdown allows 30 seconds;
- cloud authority comes from workload identity, never static keys;
- resource values are hypotheses requiring measurement;
- the Course 2 foundation remains singleton and zonal unless later evidence changes that claim.

Course 3 may change packaging. It may not silently alter these semantics to make an image easier to build.
