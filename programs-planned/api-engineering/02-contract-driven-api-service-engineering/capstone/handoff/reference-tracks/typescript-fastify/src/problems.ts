import type {
    FastifyError,
    FastifyInstance,
    FastifyReply,
    FastifyRequest,
} from "fastify";

export type ProblemIssue = {
    location: Array<string | number>;
    message: string;
    code: string;
};

export class ApiProblem extends Error {
    public constructor(
        public readonly status: number,
        public readonly title: string,
        message: string,
        public readonly slug: string,
        public readonly errors?: ProblemIssue[],
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
    const pathTokens = (item.instancePath ?? "").split("/").filter(Boolean);

    for (const token of pathTokens) {
        tokens.push(/^[0-9]+$/.test(token) ? Number(token) : token);
    }

    const missingProperty = item.params?.["missingProperty"];
    if (typeof missingProperty === "string") {
        tokens.push(missingProperty);
    }
    return tokens;
}

function problemBody(
    request: FastifyRequest,
    problem: ApiProblem,
): Record<string, unknown> {
    return {
        type: `https://api.example.test/problems/${problem.slug}`,
        title: problem.title,
        status: problem.status,
        detail: problem.message,
        instance: request.url.split("?", 1)[0],
        requestId: request.id,
        ...(problem.errors ? { errors: problem.errors } : {}),
    };
}

async function sendProblem(
    reply: FastifyReply,
    request: FastifyRequest,
    problem: ApiProblem,
): Promise<void> {
    await reply
        .code(problem.status)
        .type("application/problem+json")
        .header("X-Request-Id", request.id)
        .send(problemBody(request, problem));
}

export function installProblemHandling(app: FastifyInstance): void {
    app.setErrorHandler(
        async (
            error: FastifyError,
            request: FastifyRequest,
            reply: FastifyReply,
        ): Promise<void> => {
            if (error instanceof ApiProblem) {
                await sendProblem(reply, request, error);
                return;
            }

            const validation = (
                error as FastifyError & { validation?: ValidationItem[] }
            ).validation;
            if (validation) {
                const issues = validation.map((item): ProblemIssue => ({
                    location: validationLocation(item),
                    message: item.message ?? "Invalid value",
                    code: item.keyword ?? "validation_error",
                }));
                await sendProblem(
                    reply,
                    request,
                    new ApiProblem(
                        422,
                        "Request validation failed",
                        "One or more request values are invalid.",
                        "validation",
                        issues,
                    ),
                );
                return;
            }

            request.log.error({ err: error }, "unhandled request failure");
            await sendProblem(
                reply,
                request,
                new ApiProblem(
                    500,
                    "Internal server error",
                    "The request could not be completed.",
                    "internal",
                ),
            );
        },
    );

    app.setNotFoundHandler(async (request, reply): Promise<void> => {
        await sendProblem(
            reply,
            request,
            new ApiProblem(
                404,
                "Resource not found",
                "The requested route does not exist.",
                "not-found",
            ),
        );
    });
}
