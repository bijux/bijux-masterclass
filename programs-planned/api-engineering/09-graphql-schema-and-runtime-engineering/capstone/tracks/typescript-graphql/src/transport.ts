/** Course profile for GraphQL-over-HTTP request admission. */

export const graphResponse =
  "application/graphql-response+json";

export interface HttpRequest {
  method: string;
  accept: string;
  contentType?: string;
  operationType: "query" | "mutation" | "subscription";
}

export interface HttpDecision {
  accepted: boolean;
  status: number;
  responseContentType: string;
  reason: string;
}

export function evaluate(request: HttpRequest): HttpDecision {
  if (!request.accept.includes(graphResponse)) {
    return {
      accepted: false,
      status: 406,
      responseContentType: graphResponse,
      reason: "unsupported Accept",
    };
  }

  if (
    request.method === "GET" &&
    request.operationType !== "query"
  ) {
    return {
      accepted: false,
      status: 405,
      responseContentType: graphResponse,
      reason: "GET may not execute mutation or subscription",
    };
  }

  if (
    request.method === "POST" &&
    request.contentType !== "application/json"
  ) {
    return {
      accepted: false,
      status: 415,
      responseContentType: graphResponse,
      reason: "POST requires application/json",
    };
  }

  if (!new Set(["GET", "POST"]).has(request.method)) {
    return {
      accepted: false,
      status: 405,
      responseContentType: graphResponse,
      reason: "unsupported method",
    };
  }

  return {
    accepted: true,
    status: 200,
    responseContentType: graphResponse,
    reason: "accepted",
  };
}
