# Traffic policy package

Traffic controls preserve semantics by classifying pressure explicitly. A
quota rejection is `429`; a service that cannot admit work within its resource
budget uses a documented overload response such as `503`. Neither is silently
converted into a timeout or a successful queued request.

The executable controls cover token-bucket quotas, tenant fairness, bounded
admission queues, concurrency permits, priority classes, and deterministic
load-shedding decisions. They are single-process references; distributed
coordination belongs to a later course and must not be implied here.
