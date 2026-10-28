# TaskHarbor

TaskHarbor is the Course 4 cumulative product: a dependency-aware asynchronous job orchestrator with bounded producer invocation, typed terminal outcomes, cooperative cancellation, task and run deadlines, immutable lifecycle observations, correlation context, deterministic reporting, and a graceful executable boundary.

## Commands

```text
taskharbor inspect <manifest.json>
taskharbor run <manifest.json> [--concurrency <n>] [--policy continue|fail-fast] [--timeout-ms <n>]
taskharbor demo
taskharbor help
taskharbor version
```

## Built-in tasks

- `delay` waits cooperatively;
- `echo` returns text unchanged;
- `uppercase` returns normalized uppercase text;
- `fail` produces a deliberate domain failure.

Tasks can declare dependencies, local timeout, and priority. Priority changes selection only among simultaneously ready tasks. Final outcomes always follow manifest order.

## Architecture

The manifest validator owns trust conversion. The graph validator owns dependency legality. The scheduler owns task state and finite admission. The executor owns built-in effects. The event hub and diagnostics channel observe committed transitions. `main.ts` alone owns process signals and exit behavior.

## Verification

```bash
npm run typecheck
npm test
npm run demo
```

The test suite covers validation, graph cycles, reverse completion, priority, continue and fail-fast policies, event isolation, context propagation, deterministic rendering, and real CLI behavior. The implementation is standard-library-only.

## Deliberate limits

TaskHarbor is not a durable workflow engine, distributed queue, stream processor, or worker-thread system. Cancellation is cooperative and does not roll back committed effects. Live event order may vary among independent tasks. Those limits are part of the product contract rather than omissions hidden by the API.
