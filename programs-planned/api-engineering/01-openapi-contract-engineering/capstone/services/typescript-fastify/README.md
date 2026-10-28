# TypeScript provider

A Fastify implementation of the same canonical contract as the Python provider.

```bash
npm install
npm run typecheck
npm test
npm run dev
```

The route schemas perform runtime request validation and response serialization. TypeScript types are not treated as a substitute for runtime contract enforcement.
