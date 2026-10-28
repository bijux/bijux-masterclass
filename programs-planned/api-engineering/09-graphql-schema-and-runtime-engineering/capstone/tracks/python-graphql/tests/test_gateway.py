import unittest
from pathlib import Path

from graph_api.identity import encode_global_id
from graph_api.model import Principal, RequestContext
from graph_api.tour import build_gateway

ROOT = Path(__file__).resolve().parents[4]


class GatewayTests(unittest.TestCase):
    def setUp(self):
        self.gateway = build_gateway(ROOT)
        self.principal = Principal(
            "learner",
            "tenant-a",
            frozenset(
                {
                    "PROJECT_READ",
                    "PROJECT_WRITE",
                    "RUN_READ",
                    "RUN_WRITE",
                    "ARTIFACT_READ",
                    "DELIVERY_READ",
                }
            ),
        )
        self.context = RequestContext(self.principal, "test")

    def execute(self, name, variables):
        operation = self.gateway.registry.by_name(name)
        return self.gateway.execute(
            operation.sha256,
            variables,
            self.context,
        )

    def test_every_registered_operation_has_an_executor(self):
        variables = {
            "Viewer": {},
            "GetProjectOverview": {
                "projectId": encode_global_id("Project", "proj-1"),
                "first": 2,
            },
            "GetRun": {"runId": encode_global_id("AnalysisRun", "run-1")},
            "ListRuns": {"first": 2},
            "SearchPlatform": {"text": "run", "first": 3},
            "CreateProject": {
                "input": {"idempotencyKey": "project-key", "name": "New Study"}
            },
            "StartAnalysis": {
                "input": {
                    "idempotencyKey": "run-key",
                    "projectId": encode_global_id("Project", "proj-1"),
                    "datasetId": "dataset-x",
                    "algorithm": "qc",
                }
            },
            "CancelAnalysis": {
                "input": {
                    "runId": encode_global_id("AnalysisRun", "run-2"),
                    "expectedVersion": "2",
                }
            },
            "RunUpdates": {
                "runId": encode_global_id("AnalysisRun", "run-1"),
                "afterSequence": "3",
            },
            "NodeLookup": {
                "by": {"id": encode_global_id("Project", "proj-1")}
            },
        }
        for name, value in variables.items():
            with self.subTest(operation=name):
                result = self.execute(name, value)
                self.assertFalse(
                    result.errors
                    and result.errors[0].message == "operation has no executor"
                )

    def test_overview_batches_service_calls(self):
        result = self.execute(
            "GetProjectOverview",
            {
                "projectId": encode_global_id("Project", "proj-1"),
                "first": 2,
            },
        )
        self.assertEqual(
            result.extensions["batchCalls"],
            {"artifact": 1, "delivery": 1},
        )
        self.assertEqual(
            len(result.data["project"]["analysisRuns"]["edges"]),
            2,
        )


    def test_overview_second_page_batches_selected_runs(self):
        first = self.execute(
            "GetProjectOverview",
            {
                "projectId": encode_global_id("Project", "proj-1"),
                "first": 1,
            },
        )
        cursor = first.data["project"]["analysisRuns"]["pageInfo"]["endCursor"]
        second = self.execute(
            "GetProjectOverview",
            {
                "projectId": encode_global_id("Project", "proj-1"),
                "first": 1,
                "after": cursor,
            },
        )
        edges = second.data["project"]["analysisRuns"]["edges"]
        self.assertEqual(len(edges), 1)
        self.assertEqual(
            second.extensions["batchCalls"],
            {"artifact": 1, "delivery": 1},
        )

    def test_overview_partial_failure_has_field_specific_paths(self):
        self.gateway.artifacts.available = False
        result = self.execute(
            "GetProjectOverview",
            {
                "projectId": encode_global_id("Project", "proj-1"),
                "first": 2,
            },
        )
        paths = [error.path for error in result.errors]
        self.assertIn(
            (
                "project",
                "analysisRuns",
                "edges",
                0,
                "node",
                "artifacts",
            ),
            paths,
        )
        self.assertIsNone(
            result.data["project"]["analysisRuns"]["edges"][0]["node"][
                "artifacts"
            ]
        )

    def test_partial_artifact_failure_is_explicit(self):
        self.gateway.artifacts.available = False
        result = self.execute(
            "GetRun",
            {"runId": encode_global_id("AnalysisRun", "run-1")},
        )
        self.assertIsNone(result.data["analysisRun"]["artifacts"])
        self.assertEqual(result.errors[0].path, ("analysisRun", "artifacts"))

    def test_denied_nested_field_makes_no_artifact_call(self):
        principal = Principal("reader", "tenant-a", frozenset({"RUN_READ"}))
        context = RequestContext(principal, "denied")
        operation = self.gateway.registry.by_name("GetRun")
        result = self.gateway.execute(
            operation.sha256,
            {"runId": encode_global_id("AnalysisRun", "run-1")},
            context,
        )
        self.assertIsNone(result.data["analysisRun"]["artifacts"])
        self.assertEqual(self.gateway.artifacts.calls.count("batch_by_run"), 0)
        self.assertEqual(result.errors[0].code, "FORBIDDEN")

    def test_idempotent_mutation(self):
        variables = {
            "input": {
                "idempotencyKey": "k1",
                "projectId": encode_global_id("Project", "proj-1"),
                "datasetId": "d3",
                "algorithm": "qc",
            }
        }
        first = self.execute("StartAnalysis", variables)
        second = self.execute("StartAnalysis", variables)
        self.assertFalse(first.data["startAnalysis"]["replayed"])
        self.assertTrue(second.data["startAnalysis"]["replayed"])

    def test_changed_input_rejected(self):
        base = {
            "input": {
                "idempotencyKey": "k1",
                "projectId": encode_global_id("Project", "proj-1"),
                "datasetId": "d3",
                "algorithm": "qc",
            }
        }
        self.execute("StartAnalysis", base)
        changed = {"input": {**base["input"], "algorithm": "other"}}
        result = self.execute("StartAnalysis", changed)
        self.assertEqual(result.data["startAnalysis"]["code"], "CONFLICT")

    def test_wrong_tenant_conceals_resource(self):
        principal = Principal(
            "other",
            "tenant-b",
            frozenset({"RUN_READ", "ARTIFACT_READ", "DELIVERY_READ"}),
        )
        context = RequestContext(principal, "other")
        operation = self.gateway.registry.by_name("GetRun")
        result = self.gateway.execute(
            operation.sha256,
            {"runId": encode_global_id("AnalysisRun", "run-1")},
            context,
        )
        self.assertIsNone(result.data["analysisRun"])

    def test_high_water_cursor_excludes_newer_insert(self):
        first = self.execute("ListRuns", {"first": 1})
        cursor = first.data["analysisRuns"]["pageInfo"]["endCursor"]
        self.gateway.analysis.runs["run-new"] = {
            "id": "run-new",
            "tenantId": "tenant-a",
            "projectId": "proj-1",
            "datasetId": "data-new",
            "status": "RUNNING",
            "version": "1",
            "createdAt": "2026-08-09T10:00:00Z",
            "resultSummary": None,
        }
        continued = self.execute("ListRuns", {"first": 10, "after": cursor})
        continued_ids = {
            edge["node"]["id"]
            for edge in continued.data["analysisRuns"]["edges"]
        }
        self.assertNotIn(
            encode_global_id("AnalysisRun", "run-new"),
            continued_ids,
        )
        fresh = self.execute("ListRuns", {"first": 1})
        self.assertEqual(
            fresh.data["analysisRuns"]["edges"][0]["node"]["id"],
            encode_global_id("AnalysisRun", "run-new"),
        )

    def test_external_node_lookup(self):
        result = self.execute(
            "NodeLookup",
            {"by": {"externalId": "project/proj-1"}},
        )
        self.assertEqual(result.data["node"]["__typename"], "Project")
