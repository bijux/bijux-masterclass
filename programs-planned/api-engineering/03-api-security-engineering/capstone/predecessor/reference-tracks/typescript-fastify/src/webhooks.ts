import { URL } from "node:url";

import { canonicalJson, webhookSignature } from "./domain.js";
import { ApiProblem } from "./problems.js";

const APPROVED_HOST = "hooks.example.test";

/** Validate the logical public destination before it reaches the adapter. */
export function validateDestination(value: string): URL {
  let url: URL;
  try {
    url = new URL(value);
  } catch {
    throw invalidDestination("Webhook destination must be an absolute URL.");
  }

  if (
    url.protocol !== "https:" ||
    url.hostname !== APPROVED_HOST ||
    url.username !== "" ||
    url.password !== "" ||
    url.hash !== "" ||
    (url.port !== "" && url.port !== "443")
  ) {
    throw invalidDestination(
      "Webhook destinations must use the approved HTTPS host and port.",
    );
  }
  return url;
}

export function canonicalWebhookBody(value: unknown): Buffer {
  return Buffer.from(canonicalJson(value), "utf8");
}

export { webhookSignature };

/**
 * Course transport adapter.
 *
 * The application validates a public `https://hooks.example.test/...` URL.
 * Local exercises route only its path/query to the controlled receiver. This
 * indirection keeps the domain policy realistic without permitting arbitrary
 * network access during a self-contained lab.
 */
export class OutboundWebhookTransport {
  public constructor(private readonly trainingBase: string) {}

  private route(target: string): URL {
    const logical = validateDestination(target);
    const base = new URL(
      this.trainingBase.endsWith("/")
        ? this.trainingBase
        : `${this.trainingBase}/`,
    );
    const routed = new URL(logical.pathname.replace(/^\//, ""), base);
    routed.search = logical.search;
    return routed;
  }

  public async post(
    target: string,
    body: Uint8Array,
    headers: Readonly<Record<string, string>>,
    timeoutMilliseconds: number,
  ): Promise<number> {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), timeoutMilliseconds);
    try {
      const response = await fetch(this.route(target), {
        method: "POST",
        body,
        headers,
        redirect: "error",
        signal: controller.signal,
      });
      return response.status;
    } finally {
      clearTimeout(timer);
    }
  }
}

function invalidDestination(detail: string): ApiProblem {
  return new ApiProblem(
    422,
    "Request validation failed",
    detail,
    "validation",
  );
}
