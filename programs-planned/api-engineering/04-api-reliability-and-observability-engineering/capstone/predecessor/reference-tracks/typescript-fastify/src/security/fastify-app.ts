import Fastify from "fastify";
import { SecurityControlError } from "./errors.js";
import { parseStrictJson } from "./strict-json.js";

export function buildSecurityDemoApp() {
  const app = Fastify({ logger: false });
  app.addContentTypeParser("application/json", { parseAs: "buffer", bodyLimit: 1_048_576 }, (_request: unknown, body: Buffer, done: (error: Error | null, value?: unknown) => void) => {
    try { done(null, parseStrictJson(body)); }
    catch (error) { done(error instanceof Error ? error : new Error("strict JSON rejection")); }
  });
  app.get("/security/health", {}, async () => ({ status: "ok" }));
  app.post("/security/strict-json", {}, async (request: { body: unknown }) => ({ accepted: true, value: request.body }));
  app.setErrorHandler((error: unknown, _request: unknown, reply: { code(n:number):unknown; type(v:string):unknown; send(v:unknown):unknown }) => {
    const security = error instanceof SecurityControlError ? error : new SecurityControlError("request-rejected", "request was rejected");
    reply.code(security.status); reply.type("application/problem+json"); return reply.send({ type:`urn:analysis-security:${security.code}`, title:"Request rejected", status:security.status, detail:security.message });
  });
  return app;
}
