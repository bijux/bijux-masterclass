# Capstone Evidence Map

| Guarantee | Mechanism | Dependency-light evidence | Stronger environment evidence |
|---|---|---|---|
| graceful worker stop | signal handler and bounded loop | tour and unit test | installed systemd stop transcript |
| atomic result publication | same-directory temp, fsync, rename, directory fsync | unit tests | crash/power-loss test on selected storage |
| verified HTTPS | fixture CA, SAN, TLS 1.3 edge | PKI proof and tour | managed certificate, public/private DNS, load balancer |
| least privilege | unit/sysusers/tmpfiles policy | static and systemd verify | effective installed process credentials and negative access tests |
| bounded resources | systemd/cgroup policy | syntax and pure calculations | live cgroup throttling/OOM evidence |
| cloud replacement | handoff requirements | provider-neutral validation | live instance replacement and restore |
