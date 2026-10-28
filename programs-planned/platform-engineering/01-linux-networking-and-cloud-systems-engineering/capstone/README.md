# Atlas Host Runtime Capstone

Atlas Host Runtime is the executable substrate used throughout Course 1. It consists of a loopback-only API, a worker, an HTTPS edge, an atomic file-spool, structured evidence, and deployment configurations for systemd, nftables, nginx, cloud-init, and cloud-provider mapping.

The Python servers are teaching instruments. The course does not recommend Python's standard-library HTTP server as a production internet edge. The external nginx configuration demonstrates where a maintained reverse proxy belongs in a real deployment.

## Dependency-light tour

```bash
make tour
```

## Linux-backed checks

```bash
make linux-proof
make systemd-proof
make pki-proof
```
