import type {
  FastifyReply,
  FastifyRequest,
  preHandlerHookHandler,
} from "fastify";

import { ApiProblem } from "./problems.js";
import type { Principal } from "./types.js";

const READ_SCOPES = new Set([
  "projects:read",
  "datasets:read",
  "runs:read",
  "artifacts:read",
]);
const WRITE_SCOPES = new Set([
  "projects:write",
  "datasets:write",
  "runs:write",
  "webhooks:write",
]);
const ALL_USER_SCOPES = new Set([...READ_SCOPES, ...WRITE_SCOPES]);

type CredentialRecord = Readonly<{
  subject: string;
  scopes: ReadonlySet<string>;
  admin: boolean;
}>;

const TOKENS: Readonly<Record<string, CredentialRecord>> = {
  "learner-read": {
    subject: "learner",
    scopes: READ_SCOPES,
    admin: false,
  },
  "learner-write": {
    subject: "learner",
    scopes: ALL_USER_SCOPES,
    admin: false,
  },
  "other-owner": {
    subject: "other",
    scopes: ALL_USER_SCOPES,
    admin: false,
  },
  admin: {
    subject: "admin",
    scopes: new Set([...ALL_USER_SCOPES, "admin"]),
    admin: true,
  },
};

const API_KEYS: Readonly<Record<string, CredentialRecord>> = {
  "demo-api-key": {
    subject: "learner",
    scopes: ALL_USER_SCOPES,
    admin: false,
  },
};

const PRINCIPAL = Symbol("principal");

type AuthenticatedRequest = FastifyRequest & {
  [PRINCIPAL]?: Principal;
};

function firstHeader(
  value: string | string[] | undefined,
): string | undefined {
  return Array.isArray(value) ? value[0] : value;
}

function authenticationProblem(detail: string): ApiProblem {
  return new ApiProblem(
    401,
    "Authentication required",
    detail,
    "unauthorized",
  );
}

function authenticate(request: FastifyRequest): Principal {
  const authorization = firstHeader(request.headers.authorization);
  const apiKey = firstHeader(request.headers["x-api-key"]);
  let record: CredentialRecord | undefined;

  if (authorization !== undefined) {
    const [scheme, value] = authorization.split(" ", 2);
    if (scheme?.toLowerCase() !== "bearer" || !value) {
      throw authenticationProblem("Malformed bearer credential.");
    }
    record = TOKENS[value];
    if (!record) {
      throw authenticationProblem("Unknown bearer credential.");
    }
  } else if (apiKey !== undefined) {
    record = API_KEYS[apiKey];
    if (!record) {
      throw authenticationProblem("Unknown API key.");
    }
  } else {
    throw authenticationProblem(
      "Supply a bearer token or X-API-Key.",
    );
  }

  return {
    subject: record.subject,
    scopes: new Set(record.scopes),
    admin: record.admin,
  };
}

export function requireScopes(
  ...required: string[]
): preHandlerHookHandler {
  return async (
    request: FastifyRequest,
    _reply: FastifyReply,
  ): Promise<void> => {
    const value = authenticate(request);
    const missing = required.filter(
      (scope) => !value.scopes.has(scope),
    );
    if (missing.length > 0) {
      throw new ApiProblem(
        403,
        "Permission denied",
        `Missing required scope(s): ${missing.sort().join(", ")}.`,
        "forbidden",
      );
    }
    (request as AuthenticatedRequest)[PRINCIPAL] = value;
  };
}

export function principal(request: FastifyRequest): Principal {
  const value = (request as AuthenticatedRequest)[PRINCIPAL];
  if (!value) {
    throw new Error(
      "authenticated route executed without a principal",
    );
  }
  return value;
}
