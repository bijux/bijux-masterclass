import type { FastifyReply, FastifyRequest, preHandlerHookHandler } from "fastify";

import { ApiProblem } from "./problems.js";
import type { Principal } from "./types.js";

const readScopes = new Set([
  "projects:read",
  "datasets:read",
  "runs:read",
  "artifacts:read",
]);
const writeScopes = new Set([
  "projects:write",
  "datasets:write",
  "runs:write",
  "webhooks:write",
]);
const allUserScopes = new Set([...readScopes, ...writeScopes]);

type CredentialRecord = {
  subject: string;
  scopes: ReadonlySet<string>;
  admin: boolean;
};

const tokens: Record<string, CredentialRecord> = {
  "learner-read": { subject: "learner", scopes: readScopes, admin: false },
  "learner-write": { subject: "learner", scopes: allUserScopes, admin: false },
  "other-owner": { subject: "other", scopes: allUserScopes, admin: false },
  admin: {
    subject: "admin",
    scopes: new Set([...allUserScopes, "admin"]),
    admin: true,
  },
};

const apiKeys: Record<string, CredentialRecord> = {
  "demo-api-key": { subject: "learner", scopes: allUserScopes, admin: false },
};

const principalSymbol = Symbol("principal");

type AuthenticatedRequest = FastifyRequest & {
  [principalSymbol]?: Principal;
};

function authenticate(request: FastifyRequest): Principal {
  const authorizationHeader = request.headers.authorization;
  const authorization = Array.isArray(authorizationHeader)
    ? authorizationHeader[0]
    : authorizationHeader;
  const apiKeyHeader = request.headers["x-api-key"];
  const apiKey = Array.isArray(apiKeyHeader) ? apiKeyHeader[0] : apiKeyHeader;

  let record: CredentialRecord | undefined;
  if (authorization) {
    const [scheme, value] = authorization.split(" ", 2);
    if (scheme?.toLowerCase() !== "bearer" || !value) {
      throw new ApiProblem(401, "Authentication required", "Malformed bearer credential.", "unauthorized");
    }
    record = tokens[value];
    if (!record) {
      throw new ApiProblem(401, "Authentication required", "Unknown bearer credential.", "unauthorized");
    }
  } else if (apiKey) {
    record = apiKeys[apiKey];
    if (!record) {
      throw new ApiProblem(401, "Authentication required", "Unknown API key.", "unauthorized");
    }
  } else {
    throw new ApiProblem(
      401,
      "Authentication required",
      "Supply a bearer token or X-API-Key.",
      "unauthorized",
    );
  }

  return {
    subject: record.subject,
    scopes: new Set(record.scopes),
    admin: record.admin,
  };
}

export function requireScopes(...required: string[]): preHandlerHookHandler {
  return async (request: FastifyRequest, _reply: FastifyReply): Promise<void> => {
    const value = authenticate(request);
    const missing = required.filter((scope) => !value.scopes.has(scope));
    if (missing.length > 0) {
      throw new ApiProblem(
        403,
        "Permission denied",
        `Missing required scope(s): ${missing.sort().join(", ")}.`,
        "forbidden",
      );
    }
    (request as AuthenticatedRequest)[principalSymbol] = value;
  };
}

export function principal(request: FastifyRequest): Principal {
  const value = (request as AuthenticatedRequest)[principalSymbol];
  if (!value) {
    throw new Error("authenticated route executed without a principal");
  }
  return value;
}
