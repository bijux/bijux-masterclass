import { SecurityControlError } from "./errors.js";
import type { Decision, Principal, ResourceFacts } from "./models.js";
import type { Policy } from "./authorization.js";
import { authorize } from "./authorization.js";

export interface CredentialInputs { readonly bearerToken?: string; readonly apiKey?: string }

export function authenticateExactlyOne(
  inputs: CredentialInputs,
  bearerValidator: (value: string) => Principal,
  apiKeyValidator: (value: string) => Principal,
): Principal {
  const supplied = Number(inputs.bearerToken !== undefined) + Number(inputs.apiKey !== undefined);
  if (supplied === 0) throw new SecurityControlError("credential-required", "one credential is required", 401);
  if (supplied !== 1) throw new SecurityControlError("credential-ambiguous", "multiple credential channels are prohibited", 400);
  return inputs.bearerToken !== undefined ? bearerValidator(inputs.bearerToken) : apiKeyValidator(inputs.apiKey as string);
}

export function securityDecision(input: {
  operationId: string;
  credentials?: CredentialInputs;
  resource: ResourceFacts;
  policies: ReadonlyMap<string, Policy>;
  bearerValidator: (value: string) => Principal;
  apiKeyValidator: (value: string) => Principal;
}): { readonly principal?: Principal; readonly decision: Decision } {
  if (input.operationId === "getHealth" && input.credentials === undefined) {
    return { decision: authorize(input.operationId, undefined, input.resource, input.policies) };
  }
  if (input.credentials === undefined) throw new SecurityControlError("credential-required", "one credential is required", 401);
  const principal = authenticateExactlyOne(input.credentials, input.bearerValidator, input.apiKeyValidator);
  return { principal, decision: authorize(input.operationId, principal, input.resource, input.policies) };
}
