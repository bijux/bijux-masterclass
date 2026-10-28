# Source and Claim Notes

## Pinned baseline

The authored courses target:

- Node.js 24.19.0 LTS;
- npm 11.17.0;
- TypeScript 7.0.2;
- `@types/node` 24.13.3;
- ECMAScript modules;
- the built-in Node.js test runner.

A compatibility run on another maintained toolchain is useful evidence but is not described as proof of the pinned baseline.

## Claim classes

1. **ECMAScript rule** — runtime semantics specified by ECMAScript.
2. **TypeScript rule** — static behavior of the selected checker release.
3. **Node.js API contract** — documented behavior of the selected Node release.
4. **npm/package contract** — package-manager or package-metadata behavior.
5. **Platform-conditioned fact** — operating system, filesystem, terminal, locale, clock, or environment dependent.
6. **Observed artifact fact** — measured for named versions and inputs.
7. **Pedagogical model** — a reasoning simplification, not a formal replacement.
8. **Product policy** — a deliberate laboratory or capstone decision.

## Primary sources

- ECMAScript specification: <https://tc39.es/ecma262/>
- Node.js API: <https://nodejs.org/api/>
- Node.js ESM: <https://nodejs.org/api/esm.html>
- Node.js package entry points: <https://nodejs.org/api/packages.html#package-entry-points>
- Node.js test runner: <https://nodejs.org/api/test.html>
- Node.js event loop and timers: <https://nodejs.org/en/learn/asynchronous-work/event-loop-timers-and-nexttick>
- Node.js events: <https://nodejs.org/api/events.html>
- Node.js timers: <https://nodejs.org/api/timers.html>
- Node.js globals and AbortSignal: <https://nodejs.org/api/globals.html>
- Node.js AsyncLocalStorage: <https://nodejs.org/api/async_context.html>
- Node.js diagnostics channel: <https://nodejs.org/api/diagnostics_channel.html>
- Node.js process lifecycle: <https://nodejs.org/api/process.html>
- Node.js TypeScript support: <https://nodejs.org/api/typescript.html>
- TypeScript Handbook: <https://www.typescriptlang.org/docs/handbook/intro.html>
- Type compatibility: <https://www.typescriptlang.org/docs/handbook/type-compatibility.html>
- Generics: <https://www.typescriptlang.org/docs/handbook/2/generics.html>
- Conditional types: <https://www.typescriptlang.org/docs/handbook/2/conditional-types.html>
- Mapped types: <https://www.typescriptlang.org/docs/handbook/2/mapped-types.html>
- Template-literal types: <https://www.typescriptlang.org/docs/handbook/2/template-literal-types.html>
- Declaration files: <https://www.typescriptlang.org/docs/handbook/declaration-files/introduction.html>
- Declaration dos and don'ts: <https://www.typescriptlang.org/docs/handbook/declaration-files/do-s-and-don-ts.html>
- TypeScript compiler options: <https://www.typescriptlang.org/tsconfig/>
- npm package metadata: <https://docs.npmjs.com/cli/configuring-npm/package-json>

## Evidence boundary

A successful type check does not prove runtime property shape, descriptor attributes, private-brand legitimacy, schema acceptance, declaration/runtime alignment, package resolution, scheduling order, promise ownership, cancellation response, listener cleanup, deadline behavior, process shutdown, compatibility, persistence validity, or resource cleanup. Each claim remains tied to evidence capable of falsifying it.

## Course 5 primary Node.js sources

- Buffer and typed-array behavior: <https://nodejs.org/api/buffer.html>
- Streams and backpressure contracts: <https://nodejs.org/api/stream.html>
- Web Streams interoperability: <https://nodejs.org/api/webstreams.html>
- Files and file-handle APIs: <https://nodejs.org/api/fs.html>
- String decoding: <https://nodejs.org/api/string_decoder.html>
- Compression streams: <https://nodejs.org/api/zlib.html>
- Hashing and crypto primitives: <https://nodejs.org/api/crypto.html>
- Child processes and stdio: <https://nodejs.org/api/child_process.html>

Course 5 classifies stream thresholds, zlib internals, filesystem durability, rename behavior, child signals, and path races carefully. Node API documentation supplies the host contract; filesystem and operating-system behavior may still be platform conditioned. Product claims therefore name the intended failure model rather than treating one successful run as a universal guarantee.


## Course 6 primary Node.js sources

Course 6 uses the official Node.js API documentation for:

- `node:dns` and `dns.promises` resolution behavior;
- `node:net` TCP sockets, server addresses, half-close, timeouts, and close behavior;
- `node:dgram` UDP sockets and datagram semantics;
- `node:http` request, response, agent, method, header, timeout, and connection behavior;
- `node:https` HTTPS server and client integration;
- `node:tls` certificate verification, SNI, ALPN, and secure socket state;
- `node:http2` sessions, streams, flow control, reset, GOAWAY, and graceful close;
- `AbortController`, timers, streams, and event APIs used at lifecycle boundaries.

HTTP method, status, conditional request, entity-tag, redirect, and server-sent-event claims are treated as protocol claims and are stated narrowly. The course does not infer application idempotency from method names alone and does not treat a successful TLS handshake as application authorization.

TLS credentials included in Course 6 are local teaching fixtures. The certificate and CA are not operational recommendations, and no CA private key is distributed.
