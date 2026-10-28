# Guide — use packet capture safely and precisely

Packet capture can reveal credentials, personal data, tenant identifiers, and application payloads. Treat it as privileged evidence collection.

## Before capture

- obtain authorization for the environment and interface;
- define the exact flow, time window, and hypothesis;
- use the narrowest address/port/protocol filter;
- decide whether payload bytes are needed;
- set bounded file size, count, and retention;
- synchronize clocks across observation points;
- prepare secure storage and deletion.

## Capture at a named boundary

A capture on `any` is convenient but can show duplicate packets and obscure the interface where translation occurred. Prefer named points:

- source Pod namespace;
- source node egress device;
- tunnel device;
- destination node ingress device;
- destination Pod namespace;
- Gateway frontend and backend sockets.

## Interpret offload carefully

Checksum and segmentation offload can make captures appear to contain bad checksums or oversized segments. Record whether the capture was before or after offload processing. Packet absence can also mean the filter or namespace was wrong.

## Minimize data

Use header-only snap lengths when payload is unnecessary. Redact or encrypt retained captures. Do not commit packet captures containing secrets to the course repository.

## Cleanup

Stop capture explicitly, verify file ownership and size, extract only the required summary, then delete raw data according to the lab’s retention rule.
