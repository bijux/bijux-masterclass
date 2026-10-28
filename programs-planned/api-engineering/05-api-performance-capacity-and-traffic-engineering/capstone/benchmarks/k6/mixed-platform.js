import http from "k6/http";
import { check, sleep } from "k6";

const BASE_URL = __ENV.BASE_URL || "http://127.0.0.1:8000";
const headers = {
  Authorization: `Bearer ${__ENV.ACCESS_TOKEN || "explicit-fixture-token"}`,
  "Content-Type": "application/json",
};

export const options = {
  scenarios: {
    reads: {
      executor: "constant-arrival-rate",
      rate: Number(__ENV.READ_RATE || "80"),
      timeUnit: "1s",
      duration: __ENV.DURATION || "90s",
      preAllocatedVUs: 30,
      maxVUs: 150,
      exec: "reads",
    },
    submissions: {
      executor: "constant-arrival-rate",
      rate: Number(__ENV.SUBMIT_RATE || "4"),
      timeUnit: "1s",
      duration: __ENV.DURATION || "90s",
      preAllocatedVUs: 8,
      maxVUs: 40,
      exec: "submissions",
    },
  },
};

export function reads() {
  const response = http.get(`${BASE_URL}/analysis-runs?limit=20`, {
    headers,
    tags: { workload: "WL-MIXED", operation: "listAnalysisRuns" },
  });
  check(response, { "read accepted outcome": (r) => r.status === 200 || r.status === 429 });
}

export function submissions() {
  const key = `k6-${__VU}-${__ITER}`;
  const body = JSON.stringify({ projectId: "project-1", datasetId: "dataset-1", checksum: "sha256" });
  const response = http.post(`${BASE_URL}/analysis-runs`, body, {
    headers: { ...headers, "Idempotency-Key": key },
    tags: { workload: "WL-MIXED", operation: "createAnalysisRun" },
  });
  check(response, { "submission classified": (r) => [200, 202, 409, 429, 503].includes(r.status) });
  sleep(0.01);
}
