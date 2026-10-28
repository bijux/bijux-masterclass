# Case 3 — The probe storm

Atlas API depends on a database for write operations. A liveness endpoint returns failure whenever the database is unavailable. During a regional database incident, every API container is restarted repeatedly.

The restart storm creates secondary damage:

- connection establishment load increases;
- in-flight read requests are terminated;
- local diagnostic state disappears;
- startup work competes for CPU;
- rollout and restart alerts obscure the original dependency failure.

The liveness probe encoded the wrong question. Database availability does not prove that restarting the API process is a repair. The endpoint is split:

- `/live` checks that the process and internal event loop can make progress;
- `/ready` follows the declared traffic model and becomes false when the instance cannot safely handle normal requests;
- application responses expose controlled degradation for capabilities that remain usable.

The incident exercise captures restart count, last termination state, probe failures, database evidence, and user-journey outcomes. After the change, the same dependency failure removes instances from normal write traffic without restarting healthy processes. Recovery occurs when the dependency returns, not when kubelets happen to align.

**Lesson:** a probe is a control input. If its failure action does not repair the tested condition, the probe can amplify outages.
