# Final Verification — Course 1

This record describes the evidence executed for **Linux, Networking, and Cloud Systems Engineering 1.0.0** before the course tree was frozen into its release manifest.

## Inventory

- 67 navigated course-book pages
- approximately 42,186 course-book words
- one orientation module and 10 numbered modules
- 120 numbered exercises and 120 matching worked answers
- 10 numbered laboratories and 10 numbered evidence checkpoints
- 32 Python source, test, and proof files
- 4 systemd services and 1 timer
- 9 exact Course 2 handoff files

## Executed release evidence

```text
PASS dependency-light core proof
PASS 21 Python tests
PASS Atlas HTTPS/API/worker/edge tour — 7 checks
PASS complete process cleanup after the tour
PASS systemd unit verification with systemd-analyze 257
PASS local PKI profile and hostname-verification evidence
PASS Nginx reference configuration syntax with Nginx 1.26.3
PASS Course 2 handoff — 14 unique requirements in 9 files
PASS MkDocs navigation inventory — 67 pages
PASS 54 local course-book links
PASS Python and shell syntax checks
PASS reader-first depth, answer, lab, checkpoint, and repetition guards
```

The local tour specifically demonstrated:

1. an incorrect TLS hostname is rejected;
2. `atlas.test` is authenticated while the socket is pinned to loopback;
3. readiness checks storage and worker heartbeat state;
4. a job is accepted durably and completed by a separate worker process;
5. client-supplied forwarding identity is discarded and replaced by the trusted edge;
6. an invalid HTTP authority is rejected with `421`;
7. the worker terminates cleanly and every started process is reaped.

## Build environment

```text
Kernel:             Linux 6.18.35 x86_64
Python:             3.13.5
OpenSSL:            3.5.5
Nginx:              1.26.3
systemd tools:      257
PID 1:              supervisord
cgroup v2:          available
effective UID:      0
CAP_NET_ADMIN:      absent
CAP_SYS_ADMIN:      absent
```

The environment doctor therefore classified dependency-light and local-runtime evidence as available, but not privileged-VM or real-cloud evidence. UID 0 alone was not treated as proof of the required kernel capabilities.

## Explicitly not executed

The following routes remain part of the course but were not represented as passes:

- strict MkDocs rendering, because the documentation dependencies were unavailable;
- the network-namespace and nftables laboratory, because the environment lacked `CAP_NET_ADMIN` and `CAP_SYS_ADMIN`;
- the systemd resource-control laboratory, because systemd did not own PID 1 and no delegated manager was available;
- native nftables and cloud-init validation, because those executables were absent;
- any real-cloud IAM, metadata, DNS, load-balancer, storage, failure-domain, quota, billing, or replacement proof.

## Interpretation

The executed evidence supports the educational mechanisms and local Atlas Host Runtime behavior claimed by this release. It does not justify a statement that the package is an operated production service or that provider integrations were exercised. Those boundaries are described in `PRODUCTION-CLAIMS.md` and carried into every relevant laboratory.
