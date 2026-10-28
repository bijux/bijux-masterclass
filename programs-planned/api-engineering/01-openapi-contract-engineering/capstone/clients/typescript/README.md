# TypeScript consumer

This client deliberately separates generated contract types from transport behavior. The checked-in client uses Node's standard `fetch`, `FormData`, and `Blob`; the generated snapshot demonstrates how the same contract feeds `openapi-typescript` and `openapi-fetch`.

```bash
npm install
npm run typecheck
npm test
npm run demo -- http://127.0.0.1:8000 ./sample.csv
```

The tests verify authentication, Problem Details, multipart upload, idempotency headers, asynchronous polling, and artifact retrieval without requiring a live provider.
