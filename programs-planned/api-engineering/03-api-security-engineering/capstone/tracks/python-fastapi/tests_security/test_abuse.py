from api_security.abuse import ConcurrencyLimiter, TokenBucket


def test_shared_bucket_vectors(vector_loader):
    for case in vector_loader("abuse.json")["bucketCases"]:
        bucket=TokenBucket(case["capacity"],case["refillPerSecond"])
        for event in case["events"]:
            assert bucket.allow(now_ms=event["atMs"],cost_units=event["cost"]) is event["allow"],case["id"]


def test_permit_release_success_exception_and_idempotence():
    limiter=ConcurrencyLimiter(1)
    permit=limiter.try_acquire()
    assert permit is not None and limiter.try_acquire() is None
    permit.release(); permit.release()
    assert limiter.in_use==0
    try:
        with limiter.try_acquire():
            raise RuntimeError("fixture")
    except RuntimeError:
        pass
    assert limiter.in_use==0
