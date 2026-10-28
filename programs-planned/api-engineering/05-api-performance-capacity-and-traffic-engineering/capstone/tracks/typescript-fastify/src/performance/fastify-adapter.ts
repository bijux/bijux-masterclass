/** Illustrative Fastify integration for the framework-independent admission gate. */
import type { FastifyInstance, FastifyRequest } from "fastify";
import { AdmissionController, AdmissionRejected } from "./admission.js";

export function installPerformanceBoundary(
  app: FastifyInstance,
  controller: AdmissionController,
): void {
  app.addHook("onRequest", async (request: FastifyRequest) => {
    const operation = request.routeOptions.url ?? request.url;
    try {
      const permit = await controller.acquire(operation);
      request.performancePermit = permit;
    } catch (error) {
      if (!(error instanceof AdmissionRejected)) throw error;
      throw app.httpErrors.serviceUnavailable("request cannot be admitted now", {
        headers: { "retry-after": String(error.retryAfterSeconds) },
      });
    }
  });
  app.addHook("onResponse", async (request) => {
    request.performancePermit?.release();
  });
  app.addHook("onError", async (request) => {
    request.performancePermit?.release();
  });
}

declare module "fastify" {
  interface FastifyRequest {
    performancePermit?: { release(): void };
  }
}
