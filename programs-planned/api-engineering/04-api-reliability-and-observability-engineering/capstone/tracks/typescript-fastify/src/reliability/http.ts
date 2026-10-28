export interface HttpOutcome {
  readonly eligibility: "eligible" | "excluded";
  readonly outcome: "good" | "bad" | "neutral";
}

export function classifyHttpOutcome(operation: string, status: number): HttpOutcome {
  if (!Number.isSafeInteger(status) || status < 100 || status > 599) {
    throw new Error("status must be an HTTP status code");
  }
  if (operation.startsWith("internal") || operation.startsWith("/internal/")) {
    return { eligibility: "excluded", outcome: "neutral" };
  }
  if (status >= 200 && status < 400) {
    return { eligibility: "eligible", outcome: "good" };
  }
  if ([408, 425, 429].includes(status) || status >= 500) {
    return { eligibility: "eligible", outcome: "bad" };
  }
  return { eligibility: "excluded", outcome: "neutral" };
}
