import type { FastifyError, FastifyInstance, FastifyReply, FastifyRequest } from "fastify";

export class ApiProblem extends Error {
  public constructor(
    public readonly status: number,
    public readonly title: string,
    message: string,
    public readonly slug: string,
    public readonly errors?: Array<{ location: Array<string | number>; message: string; code: string }>,
  ) {
    super(message);
    this.name = "ApiProblem";
  }
}

type ValidationItem = {
  instancePath?: string;
  schemaPath?: string;
  keyword?: string;
  message?: string;
  params?: Record<string, unknown>;
};

function validationLocation(item: ValidationItem): Array<string | number> {
  const tokens: Array<string | number> = ["body"];
  for (const token of (item.instancePath ?? "").split("/").filter(Boolean)) {
    tokens.push(/^[0-9]+$/.test(token) ? Number(token) : token);
  }
  const missing = item.params?.["missingProperty"];
  if (typeof missing === "string") {
    tokens.push(missing);
  }
  return tokens;
}

export function installProblemHandling(app: FastifyInstance): void {
  app.setErrorHandler(
    async (error: FastifyError, request: FastifyRequest, reply: FastifyReply) => {
      if (error instanceof ApiProblem) {
        await reply
          .code(error.status)
          .type("application/problem+json")
          .header("X-Request-Id", request.id)
          .send({
            type: `https://api.example.test/problems/${error.slug}`,
            title: error.title,
            status: error.status,
            detail: error.message,
            instance: request.url.split("?", 1)[0],
            requestId: request.id,
            ...(error.status === 422
              ? {
                  errors: error.errors ?? [
                    {
                      location: ["body"],
                      message: error.message,
                      code: "validation_error",
                    },
                  ],
                }
              : {}),
          });
        return;
      }

      const validation = (error as FastifyError & { validation?: ValidationItem[] }).validation;
      if (validation) {
        await reply
          .code(422)
          .type("application/problem+json")
          .header("X-Request-Id", request.id)
          .send({
            type: "https://api.example.test/problems/validation",
            title: "Request validation failed",
            status: 422,
            detail: "One or more request values are invalid.",
            instance: request.url.split("?", 1)[0],
            requestId: request.id,
            errors: validation.map((item) => ({
              location: validationLocation(item),
              message: item.message ?? "Invalid value",
              code: item.keyword ?? "validation_error",
            })),
          });
        return;
      }

      request.log.error({ err: error }, "unhandled request failure");
      await reply
        .code(500)
        .type("application/problem+json")
        .header("X-Request-Id", request.id)
        .send({
          type: "https://api.example.test/problems/internal",
          title: "Internal server error",
          status: 500,
          detail: "The request could not be completed.",
          instance: request.url.split("?", 1)[0],
          requestId: request.id,
        });
    },
  );

  app.setNotFoundHandler(async (request, reply) => {
    await reply
      .code(404)
      .type("application/problem+json")
      .header("X-Request-Id", request.id)
      .send({
        type: "https://api.example.test/problems/not-found",
        title: "Resource not found",
        status: 404,
        detail: "The requested route does not exist.",
        instance: request.url.split("?", 1)[0],
        requestId: request.id,
      });
  });
}
