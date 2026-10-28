import http from "k6/http";
import { check } from "k6";

const BASE_URL = __ENV.BASE_URL || "http://127.0.0.1:8000";
const RATE = Number(__ENV.RATE || "40");

export const options = {
  scenarios: {
    run_list_open: {
      executor: "constant-arrival-rate",
      rate: RATE,
      timeUnit: "1s",
      duration: __ENV.DURATION || "60s",
      preAllocatedVUs: Number(__ENV.PREALLOCATED_VUS || "20"),
      maxVUs: Number(__ENV.MAX_VUS || "100"),
    },
  },
  thresholds: {
    checks: ["rate==1"],
    http_req_failed: ["rate<0.005"],
  },
};

export default function () {
  const response = http.get(`${BASE_URL}/analysis-runs?limit=50&status=completed`, {
    headers: { Authorization: `Bearer ${__ENV.ACCESS_TOKEN || "explicit-fixture-token"}` },
    tags: { workload: "WL-RUN-LIST", operation: "listAnalysisRuns" },
  });
  check(response, {
    "status is 200": (r) => r.status === 200,
    "response has items": (r) => Array.isArray(r.json("items")),
  });
}
