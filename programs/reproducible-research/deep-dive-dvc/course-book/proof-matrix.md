<a id="top"></a>

# Proof Matrix

This page maps the course's main claims to the commands and files that prove them.

Use it when you care about a concept but want the fastest evidence route.

---

## Core State Claims

| Claim | Command | File surfaces |
| --- | --- | --- |
| data identity is not only a path name | `make -C capstone walkthrough` | `capstone/data/raw/service_incidents.csv`, `capstone/dvc.lock` |
| the pipeline declares the real change surface | `make -C capstone repro` | `capstone/dvc.yaml`, `capstone/dvc.lock` |
| params are part of recorded execution meaning | `make -C capstone verify` | `capstone/params.yaml`, `capstone/dvc.lock` |
| metrics are reviewable state, not only console output | `make -C capstone verify` | `capstone/metrics/metrics.json`, `capstone/publish/v1/metrics.json` |
| promoted outputs are smaller than internal repository state | `make -C capstone tour` | `capstone/publish/v1/`, `capstone/state/`, `capstone/README.md` |

[Back to top](#top)

---

## Operational Claims

| Claim | Command | File surfaces |
| --- | --- | --- |
| the repository can rebuild its promoted contract | `make -C capstone verify` | `capstone/publish/v1/manifest.json`, `capstone/src/incident_escalation_capstone/verify.py` |
| experiments can vary parameters without mutating the baseline contract | `dvc exp run --cwd capstone` | `capstone/params.yaml`, `capstone/dvc.lock` |
| another person can run the same proof targets through the public interface | `make -C capstone help` | `capstone/Makefile` |
| remote-backed recovery still works after local loss | `make -C capstone recovery-drill` | `capstone/.dvc-remote/`, `capstone/publish/v1/` |
| the full repository can defend itself under review | `make -C capstone confirm` | `capstone/README.md`, `capstone/dvc.yaml`, `capstone/dvc.lock` |

[Back to top](#top)

---

## Review Questions

| Question | Best first command | Best first file |
| --- | --- | --- |
| what exactly changed between declaration and recorded execution | `make -C capstone walkthrough` | `capstone/dvc.lock` |
| which parameters are safe to compare across runs | `make -C capstone verify` | `capstone/params.yaml` |
| which artifacts are safe for downstream trust | `make -C capstone tour` | `capstone/publish/v1/manifest.json` |
| which state survives local cache loss | `make -C capstone recovery-drill` | `capstone/README.md` |
| what should I inspect before migration | `make -C capstone confirm` | `capstone/dvc.yaml` |

[Back to top](#top)

---

## Companion Pages

The most useful companion pages for this matrix are:

* [`command-guide.md`](command-guide.md)
* [`authority-map.md`](authority-map.md)
* [`practice-map.md`](practice-map.md)
* [`capstone-file-guide.md`](capstone-file-guide.md)

[Back to top](#top)
