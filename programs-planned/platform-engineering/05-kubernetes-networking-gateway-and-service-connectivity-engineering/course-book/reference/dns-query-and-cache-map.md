# DNS query and cache map

For each observed lookup record:

```text
application input name
search domains and ndots
expanded candidate
record type
resolver/server
transport UDP/TCP
response code
answer/authority
TTL
cache layer and expiry
selected address
```

Useful distinctions:

- NXDOMAIN: name does not exist;
- NOERROR/no data: name exists but no records of requested type;
- SERVFAIL: server could not complete resolution;
- timeout: no accepted response before deadline;
- truncated UDP: client may retry over TCP.

A normal Service and a headless Service publish different records. A correct answer proves discovery only; connect and TLS evidence remain separate.
