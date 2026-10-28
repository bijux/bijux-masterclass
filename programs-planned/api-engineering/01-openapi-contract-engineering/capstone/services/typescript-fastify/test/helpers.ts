import type { FastifyInstance } from "fastify";

export const writeHeaders = {
  authorization: "Bearer learner-write",
};

export function multipartFile(
  fileName: string,
  contentType: string,
  content: string,
): { payload: Buffer; headers: Record<string, string> } {
  const boundary = "----bijux-openapi-course";
  const payload = Buffer.from(
    [
      `--${boundary}`,
      `Content-Disposition: form-data; name="file"; filename="${fileName}"`,
      `Content-Type: ${contentType}`,
      "",
      content,
      `--${boundary}--`,
      "",
    ].join("\r\n"),
  );
  return {
    payload,
    headers: {
      "content-type": `multipart/form-data; boundary=${boundary}`,
      "content-length": String(payload.length),
    },
  };
}

export async function createReadyDataset(
  app: FastifyInstance,
): Promise<{ projectId: string; datasetId: string }> {
  const project = await app.inject({
    method: "POST",
    url: "/projects",
    headers: writeHeaders,
    payload: { name: "Test project" },
  });
  if (project.statusCode !== 201) {
    throw new Error(project.body);
  }
  const projectId = project.json<{ id: string }>().id;

  const dataset = await app.inject({
    method: "POST",
    url: `/projects/${projectId}/datasets`,
    headers: writeHeaders,
    payload: {
      name: "reads",
      source: {
        kind: "local-file",
        fileName: "reads.csv",
        mediaType: "text/csv",
      },
    },
  });
  if (dataset.statusCode !== 201) {
    throw new Error(dataset.body);
  }
  const datasetId = dataset.json<{ id: string }>().id;

  const upload = multipartFile("reads.csv", "text/csv", "sample,value\nA,1\n");
  const uploaded = await app.inject({
    method: "POST",
    url: `/datasets/${datasetId}/content`,
    headers: { ...writeHeaders, ...upload.headers },
    payload: upload.payload,
  });
  if (uploaded.statusCode !== 201) {
    throw new Error(uploaded.body);
  }
  return { projectId, datasetId };
}
