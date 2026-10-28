# Teaching notes by module

1. Reject messages without an owner, even when they look useful. Ask which transaction proves the fact.
2. Keep event type distinct from broker subject. Make learners reverse send/receive from the application perspective.
3. Inject expired acknowledgements before discussing delivery marketing terms.
4. Force the relay crash after broker acceptance; otherwise inbox deduplication remains abstract.
5. Compare candidates against retained bytes, not only the latest producer.
6. Make command identity and timeout generation explicit in process managers.
7. Delay an event across a window boundary so processing-time logic visibly fails.
8. Attempt cross-tenant publication and include a sensitive payload field.
9. Use one permanent and one transient failure; require different dispositions.
10. Reject at least one technically valid release for incomplete replay, security, or operational evidence.

Do not let learners substitute a vendor dashboard for durable effect evidence. Do not reward a claim of exactly-once delivery. The strongest acceptable claim is one committed effect under a named deduplication identity and transaction boundary.
