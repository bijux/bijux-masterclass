import { AnalysisClient } from "./client.js";

const [baseUrl = "http://127.0.0.1:8000", datasetPath] = process.argv.slice(2);
if (!datasetPath) {
  throw new Error("usage: npm run demo -- <base-url> <dataset-path>");
}

const bearerToken = process.env["ANALYSIS_API_TOKEN"];
const apiKey = process.env["ANALYSIS_API_KEY"];
if (Boolean(bearerToken) === Boolean(apiKey)) {
  throw new Error(
    "configure exactly one of ANALYSIS_API_TOKEN or ANALYSIS_API_KEY",
  );
}

const client = new AnalysisClient(
  baseUrl,
  bearerToken !== undefined ? { bearerToken } : { apiKey: apiKey! },
);
const result = await client.completeWorkflow(
  "TypeScript client demonstration",
  datasetPath,
  `typescript-demo-${Date.now()}`,
);
console.log(JSON.stringify(result, null, 2));
