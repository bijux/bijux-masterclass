from atlas_net.dns import DNSAuthority, DNSCache

from common import emit, record


name = "atlas-api.atlas-system.svc.cluster.local"
authority = DNSAuthority()
original_client = DNSCache(authority)

initial = original_client.query(name, "A", now=0)
authority.set(name, "A", ["10.96.0.10"], ttl=30)

# The original client retains its negative answer until the negative TTL expires.
cached_after_create = original_client.query(name, "A", now=5)
fresh_client = DNSCache(authority).query(name, "A", now=5)
after_negative_expiry = original_client.query(name, "A", now=11)

emit(
    "module-04-dns-cache.json",
    {
        "initial": record(initial),
        "cachedAfterCreate": record(cached_after_create),
        "freshClient": record(fresh_client),
        "afterNegativeExpiry": record(after_negative_expiry),
        "trace": original_client.trace,
    },
)
