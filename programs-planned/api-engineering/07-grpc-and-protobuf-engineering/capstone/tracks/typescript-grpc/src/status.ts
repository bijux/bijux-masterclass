export type GrpcStatus =
  | "OK" | "CANCELLED" | "UNKNOWN" | "INVALID_ARGUMENT"
  | "DEADLINE_EXCEEDED" | "NOT_FOUND" | "ALREADY_EXISTS"
  | "PERMISSION_DENIED" | "RESOURCE_EXHAUSTED"
  | "FAILED_PRECONDITION" | "ABORTED" | "UNAUTHENTICATED"
  | "UNAVAILABLE" | "INTERNAL";

export type AppError =
  | { kind: "invalid"; field?: string }
  | { kind: "not-found" }
  | { kind: "unauthenticated" }
  | { kind: "denied" }
  | { kind: "precondition" }
  | { kind: "conflict" }
  | { kind: "idempotency-conflict" }
  | { kind: "exhausted" };

export function statusFor(error: AppError): GrpcStatus {
  switch (error.kind) {
    case "invalid": return "INVALID_ARGUMENT";
    case "not-found": return "NOT_FOUND";
    case "unauthenticated": return "UNAUTHENTICATED";
    case "denied": return "PERMISSION_DENIED";
    case "precondition": return "FAILED_PRECONDITION";
    case "conflict": return "ABORTED";
    case "idempotency-conflict": return "ALREADY_EXISTS";
    case "exhausted": return "RESOURCE_EXHAUSTED";
  }
}

export function safeDetail(error: AppError): Readonly<Record<string, string>> {
  const detail: Record<string, string> = { reason: error.kind };
  if (error.kind === "invalid" && error.field !== undefined) {
    detail.field = error.field;
  }
  return detail;
}
