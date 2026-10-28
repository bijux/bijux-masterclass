# TypeScript Fastify Reference Track

This is the complete TypeScript reference for the course capstone. It uses Fastify, TypeBox, node-postgres, one PostgreSQL migration history, a database-backed worker lease, a content-addressed filesystem adapter, and a transactional webhook outbox.

The learner is not required to rewrite the Python track. Select this track with `TRACK=typescript` and use the Python track as comparative evidence.

## Local commands

```bash
npm install
npm run build
npm run core:test
npm test
npm run migrate
npm run dev
npm run worker
```

The application owns HTTP composition. `AnalysisService` owns use-case coordination. `PostgresRepository` owns transaction and query behavior. The worker uses the repository's lease-generation predicates so an expired worker cannot publish state after a replacement has reclaimed the job.
