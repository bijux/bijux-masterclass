# Atlas Host Runtime Architecture

This document supports the course book; it is not a substitute for it.

Atlas exposes one verified HTTPS edge, one loopback API, one worker, and a filesystem spool. The edge, API, and worker are separately supervised and separately authorized. Durable state lives under the declared state directory. Runtime evidence and heartbeats are reboot-ephemeral. The deployment authority owns immutable code, configuration, units, firewall policy, and certificate rotation.

The Python edge is a semantic fixture for local proof. The Nginx configuration is the maintained proxy reference. Production adoption requires environment-specific packaging, identity, secret delivery, logging, capacity, and support decisions.
