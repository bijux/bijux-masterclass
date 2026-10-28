from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Iterable

from .cost import CostPolicy, analyze
from .cursor import (
    CursorCodec,
    CursorState,
    audience_hash,
    normalized_filter_hash,
)
from .identity import decode_global_id, encode_global_id
from .loader import BatchLoader
from .model import (
    AuthorizationError,
    ConflictError,
    DownstreamUnavailable,
    ExecutionResult,
    GraphError,
    PreconditionFailed,
    RequestContext,
    ValidationError,
)
from .operation import parse_document
from .persisted import PersistedOperationRegistry
from .policy import require_field
from .services import (
    AnalysisControlClient,
    ArtifactServiceClient,
    NotificationServiceClient,
)
from .subscription import ResumableSubscription, SubscriptionEvent

SortKey = tuple[str, str]


@dataclass
class AnalysisGraphGateway:
    registry: PersistedOperationRegistry
    analysis: AnalysisControlClient
    artifacts: ArtifactServiceClient
    notifications: NotificationServiceClient
    cursor_codec: CursorCodec
    cost_policy: CostPolicy = CostPolicy()
    cursor_ttl_seconds: int = 3_600

    def execute(
        self,
        operation_hash: str,
        variables: dict[str, Any],
        context: RequestContext,
    ) -> ExecutionResult:
        """Execute one governed operation through lookup, admission, and dispatch."""
        try:
            operation = self.registry.get(operation_hash)
            document = parse_document(operation.document)
            report = analyze(
                document,
                operation_name=operation.name,
                variables=variables,
                policy=self.cost_policy,
            )
            method = getattr(self, f"_op_{operation.name}", None)
            if method is None:
                raise ValidationError("operation has no executor")
            result: ExecutionResult = method(variables, context)
            return ExecutionResult(
                result.data,
                result.errors,
                {
                    "cost": report.estimated_cost,
                    "serviceFanout": report.service_fanout,
                    **result.extensions,
                },
            )
        except AuthorizationError:
            return ExecutionResult(
                None,
                (GraphError("Not authorized", (), "FORBIDDEN"),),
            )
        except ValidationError as exc:
            return ExecutionResult(
                None,
                (GraphError(str(exc), (), "GRAPHQL_VALIDATION_FAILED"),),
            )
        except DownstreamUnavailable as exc:
            return ExecutionResult(
                None,
                (
                    GraphError(
                        "A required source is temporarily unavailable",
                        (),
                        "DOWNSTREAM_UNAVAILABLE",
                        exc.service,
                    ),
                ),
            )

    @staticmethod
    def _project_node(project: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": encode_global_id("Project", project["id"]),
            "name": project["name"],
            "version": project["version"],
        }

    @staticmethod
    def _run_node(run: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": encode_global_id("AnalysisRun", run["id"]),
            "projectId": encode_global_id("Project", run["projectId"]),
            "datasetId": run["datasetId"],
            "status": run["status"],
            "version": run["version"],
            "createdAt": run["createdAt"],
            "resultSummary": run["resultSummary"],
        }

    @staticmethod
    def _artifact_node(artifact: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": encode_global_id("Artifact", artifact["id"]),
            "runId": encode_global_id("AnalysisRun", artifact["runId"]),
            "mediaType": artifact["mediaType"],
            "size": artifact["size"],
            "sha256": artifact["sha256"],
            "downloadUrl": artifact["downloadUrl"],
        }

    def _connection(
        self,
        *,
        values: Iterable[dict[str, Any]],
        key_of: Callable[[dict[str, Any]], SortKey],
        node_of: Callable[[dict[str, Any]], dict[str, Any]],
        scope: str,
        filter_value: dict[str, object],
        first: int,
        after: str | None,
        context: RequestContext,
    ) -> dict[str, Any]:
        if first < 1 or first > self.cost_policy.max_page_size:
            raise ValidationError(
                f"first outside 1..{self.cost_policy.max_page_size}"
            )

        ordered = sorted(values, key=key_of, reverse=True)
        filter_hash = normalized_filter_hash(filter_value)
        caller_hash = audience_hash(context.principal)

        if after is None:
            if not ordered:
                return {
                    "edges": [],
                    "pageInfo": {"hasNextPage": False, "endCursor": None},
                }
            high_water = key_of(ordered[0])
            after_key: SortKey | None = None
        else:
            state = self.cursor_codec.decode(
                after,
                tenant_id=context.principal.tenant_id,
                audience_hash=caller_hash,
                scope=scope,
                filter_hash=filter_hash,
                now_epoch=context.now_epoch,
            )
            high_water = state.high_water_key
            after_key = state.after_key

        eligible = [
            value
            for value in ordered
            if key_of(value) <= high_water
            and (after_key is None or key_of(value) < after_key)
        ]
        selected = eligible[: first + 1]
        page = selected[:first]
        has_next_page = len(selected) > first

        edges: list[dict[str, Any]] = []
        for value in page:
            key = key_of(value)
            cursor = self.cursor_codec.encode(
                CursorState(
                    tenant_id=context.principal.tenant_id,
                    audience_hash=caller_hash,
                    scope=scope,
                    filter_hash=filter_hash,
                    after_primary=key[0],
                    after_tiebreaker=key[1],
                    high_water_primary=high_water[0],
                    high_water_tiebreaker=high_water[1],
                    expires_at=context.now_epoch + self.cursor_ttl_seconds,
                )
            )
            edges.append({"cursor": cursor, "node": node_of(value)})

        return {
            "edges": edges,
            "pageInfo": {
                "hasNextPage": has_next_page,
                "endCursor": edges[-1]["cursor"] if edges else None,
            },
        }

    def _authorized_artifacts(
        self,
        run: dict[str, Any],
        context: RequestContext,
        path: tuple[str | int, ...],
    ) -> tuple[list[dict[str, Any]] | None, GraphError | None]:
        try:
            require_field(
                context.principal,
                "AnalysisRun.artifacts",
                resource_tenant=run["tenantId"],
            )
        except AuthorizationError:
            return None, GraphError("Not authorized", path, "FORBIDDEN")
        try:
            values = self.artifacts.batch_by_run(
                context.principal, [run["id"]]
            ).get(run["id"], [])
            return [self._artifact_node(value) for value in values], None
        except DownstreamUnavailable as exc:
            return None, GraphError(
                "Artifact data is temporarily unavailable",
                path,
                "DOWNSTREAM_UNAVAILABLE",
                exc.service,
            )

    def _authorized_delivery(
        self,
        run: dict[str, Any],
        context: RequestContext,
        path: tuple[str | int, ...],
    ) -> tuple[dict[str, Any] | None, GraphError | None]:
        try:
            require_field(
                context.principal,
                "AnalysisRun.deliverySummary",
                resource_tenant=run["tenantId"],
            )
        except AuthorizationError:
            return None, GraphError("Not authorized", path, "FORBIDDEN")
        try:
            value = self.notifications.batch_by_run(
                context.principal, [run["id"]]
            ).get(run["id"])
            return value, None
        except DownstreamUnavailable as exc:
            return None, GraphError(
                "Delivery data is temporarily unavailable",
                path,
                "DOWNSTREAM_UNAVAILABLE",
                exc.service,
            )

    def _op_Viewer(
        self, variables: dict[str, Any], context: RequestContext
    ) -> ExecutionResult:
        principal = context.principal
        return ExecutionResult(
            {
                "viewer": {
                    "subject": principal.subject,
                    "tenantId": principal.tenant_id,
                    "permissions": sorted(principal.permissions),
                }
            }
        )

    def _op_GetProjectOverview(
        self, variables: dict[str, Any], context: RequestContext
    ) -> ExecutionResult:
        principal = context.principal
        require_field(principal, "Query.project")
        type_name, project_id = decode_global_id(variables["projectId"])
        if type_name != "Project":
            raise ValidationError("projectId has the wrong global identifier type")

        project = self.analysis.get_project(principal, project_id)
        if project is None:
            return ExecutionResult({"project": None})

        runs = self.analysis.list_runs(principal, project_id=project_id)
        connection = self._connection(
            values=runs,
            key_of=lambda run: (run["createdAt"], run["id"]),
            node_of=self._run_node,
            scope="Project.analysisRuns",
            filter_value={"projectId": project_id},
            first=int(variables.get("first", 20)),
            after=variables.get("after"),
            context=context,
        )

        errors: list[GraphError] = []
        artifact_loader = BatchLoader(
            lambda keys: self.artifacts.batch_by_run(principal, keys)
        )
        delivery_loader = BatchLoader(
            lambda keys: self.notifications.batch_by_run(principal, keys)
        )
        run_by_id = {run["id"]: run for run in runs}
        selected_run_ids = [
            decode_global_id(edge["node"]["id"])[1]
            for edge in connection["edges"]
        ]
        artifact_tokens: dict[str, Any] = {}
        delivery_tokens: dict[str, Any] = {}

        artifact_allowed = "ARTIFACT_READ" in principal.permissions
        delivery_allowed = "DELIVERY_READ" in principal.permissions
        artifact_failed_service: str | None = None
        delivery_failed_service: str | None = None

        if artifact_allowed:
            artifact_tokens = {
                run_id: artifact_loader.load(run_id)
                for run_id in selected_run_ids
            }
            try:
                artifact_loader.dispatch()
            except DownstreamUnavailable as exc:
                artifact_failed_service = exc.service

        if delivery_allowed:
            delivery_tokens = {
                run_id: delivery_loader.load(run_id)
                for run_id in selected_run_ids
            }
            try:
                delivery_loader.dispatch()
            except DownstreamUnavailable as exc:
                delivery_failed_service = exc.service

        for index, edge in enumerate(connection["edges"]):
            _, local_id = decode_global_id(edge["node"]["id"])
            run = run_by_id[local_id]
            artifact_path = (
                "project",
                "analysisRuns",
                "edges",
                index,
                "node",
                "artifacts",
            )
            delivery_path = (
                "project",
                "analysisRuns",
                "edges",
                index,
                "node",
                "deliverySummary",
            )

            if not artifact_allowed:
                edge["node"]["artifacts"] = None
                errors.append(GraphError("Not authorized", artifact_path, "FORBIDDEN"))
            elif artifact_failed_service is not None:
                edge["node"]["artifacts"] = None
                errors.append(
                    GraphError(
                        "Artifact data is temporarily unavailable",
                        artifact_path,
                        "DOWNSTREAM_UNAVAILABLE",
                        artifact_failed_service,
                    )
                )
            else:
                values = artifact_tokens[run["id"]].get() or []
                edge["node"]["artifacts"] = [
                    self._artifact_node(value) for value in values
                ]

            if not delivery_allowed:
                edge["node"]["deliverySummary"] = None
                errors.append(GraphError("Not authorized", delivery_path, "FORBIDDEN"))
            elif delivery_failed_service is not None:
                edge["node"]["deliverySummary"] = None
                errors.append(
                    GraphError(
                        "Delivery data is temporarily unavailable",
                        delivery_path,
                        "DOWNSTREAM_UNAVAILABLE",
                        delivery_failed_service,
                    )
                )
            else:
                edge["node"]["deliverySummary"] = delivery_tokens[
                    run["id"]
                ].get()

        project_node = self._project_node(project)
        project_node["analysisRuns"] = connection
        return ExecutionResult(
            {"project": project_node},
            tuple(errors),
            {
                "batchCalls": {
                    "artifact": artifact_loader.dispatches,
                    "delivery": delivery_loader.dispatches,
                }
            },
        )

    def _op_GetRun(
        self, variables: dict[str, Any], context: RequestContext
    ) -> ExecutionResult:
        principal = context.principal
        require_field(principal, "Query.analysisRun")
        type_name, run_id = decode_global_id(variables["runId"])
        if type_name != "AnalysisRun":
            raise ValidationError("runId has the wrong global identifier type")

        run = self.analysis.get_run(principal, run_id)
        if run is None:
            return ExecutionResult({"analysisRun": None})

        node = self._run_node(run)
        errors: list[GraphError] = []
        artifacts, artifact_error = self._authorized_artifacts(
            run, context, ("analysisRun", "artifacts")
        )
        delivery, delivery_error = self._authorized_delivery(
            run, context, ("analysisRun", "deliverySummary")
        )
        node["artifacts"] = artifacts
        node["deliverySummary"] = delivery
        if artifact_error:
            errors.append(artifact_error)
        if delivery_error:
            errors.append(delivery_error)
        return ExecutionResult({"analysisRun": node}, tuple(errors))

    def _op_ListRuns(
        self, variables: dict[str, Any], context: RequestContext
    ) -> ExecutionResult:
        principal = context.principal
        require_field(principal, "Query.analysisRun")
        filter_value = dict(variables.get("filter") or {})
        project_id: str | None = None
        if filter_value.get("projectId"):
            type_name, project_id = decode_global_id(filter_value["projectId"])
            if type_name != "Project":
                raise ValidationError("filter.projectId has the wrong type")
            filter_value["projectId"] = project_id

        values = self.analysis.list_runs(
            principal,
            project_id=project_id,
            status=filter_value.get("status"),
        )
        connection = self._connection(
            values=values,
            key_of=lambda run: (run["createdAt"], run["id"]),
            node_of=self._run_node,
            scope="Query.analysisRuns",
            filter_value=filter_value,
            first=int(variables.get("first", 20)),
            after=variables.get("after"),
            context=context,
        )
        return ExecutionResult({"analysisRuns": connection})

    def _op_SearchPlatform(
        self, variables: dict[str, Any], context: RequestContext
    ) -> ExecutionResult:
        text = str(variables["text"]).strip()
        if not text or len(text) > 200:
            raise ValidationError("search text must contain 1..200 characters")

        principal = context.principal
        values = self.analysis.search(principal, text)
        if "ARTIFACT_READ" in principal.permissions:
            values.extend(
                {"type": "Artifact", "value": value}
                for value in self.artifacts.search(principal, text)
            )

        def key_of(item: dict[str, Any]) -> SortKey:
            type_name = item["type"]
            value = item["value"]
            haystack = " ".join(str(part) for part in value.values()).casefold()
            score = 3 if haystack.startswith(text.casefold()) else 2
            return (f"{score:03d}", f"{type_name}:{value['id']}")

        def node_of(item: dict[str, Any]) -> dict[str, Any]:
            if item["type"] == "Project":
                return {"__typename": "Project", **self._project_node(item["value"])}
            if item["type"] == "AnalysisRun":
                return {
                    "__typename": "AnalysisRun",
                    **self._run_node(item["value"]),
                }
            return {
                "__typename": "Artifact",
                **self._artifact_node(item["value"]),
            }

        connection = self._connection(
            values=values,
            key_of=key_of,
            node_of=node_of,
            scope="Query.search",
            filter_value={"text": text.casefold()},
            first=int(variables.get("first", 20)),
            after=variables.get("after"),
            context=context,
        )
        return ExecutionResult({"search": connection})

    def _op_CreateProject(
        self, variables: dict[str, Any], context: RequestContext
    ) -> ExecutionResult:
        principal = context.principal
        require_field(principal, "Mutation.createProject")
        value = variables["input"]
        try:
            project, replayed = self.analysis.create_project(
                principal,
                key=value["idempotencyKey"],
                name=value["name"],
            )
            return ExecutionResult(
                {
                    "createProject": {
                        "clientMutationId": value.get("clientMutationId"),
                        "project": self._project_node(project),
                        "replayed": replayed,
                    }
                }
            )
        except ConflictError:
            return ExecutionResult(
                {
                    "createProject": {
                        "clientMutationId": value.get("clientMutationId"),
                        "code": "CONFLICT",
                        "message": "Idempotency key is bound to another input",
                        "field": "idempotencyKey",
                    }
                }
            )

    def _op_StartAnalysis(
        self, variables: dict[str, Any], context: RequestContext
    ) -> ExecutionResult:
        principal = context.principal
        require_field(principal, "Mutation.startAnalysis")
        value = variables["input"]
        type_name, project_id = decode_global_id(value["projectId"])
        if type_name != "Project":
            raise ValidationError("projectId has the wrong global identifier type")
        try:
            run, replayed = self.analysis.start_analysis(
                principal,
                key=value["idempotencyKey"],
                project_id=project_id,
                dataset_id=value["datasetId"],
                algorithm=value["algorithm"],
            )
            return ExecutionResult(
                {
                    "startAnalysis": {
                        "clientMutationId": value.get("clientMutationId"),
                        "replayed": replayed,
                        "run": self._run_node(run),
                    }
                }
            )
        except ConflictError:
            return ExecutionResult(
                {
                    "startAnalysis": {
                        "clientMutationId": value.get("clientMutationId"),
                        "code": "CONFLICT",
                        "message": "Idempotency key is bound to another input",
                        "field": "idempotencyKey",
                    }
                }
            )
        except KeyError:
            return ExecutionResult(
                {
                    "startAnalysis": {
                        "clientMutationId": value.get("clientMutationId"),
                        "code": "NOT_FOUND",
                        "message": "Project was not found",
                        "field": "projectId",
                    }
                }
            )

    def _op_CancelAnalysis(
        self, variables: dict[str, Any], context: RequestContext
    ) -> ExecutionResult:
        principal = context.principal
        require_field(principal, "Mutation.cancelAnalysis")
        value = variables["input"]
        type_name, run_id = decode_global_id(value["runId"])
        if type_name != "AnalysisRun":
            raise ValidationError("runId has the wrong global identifier type")
        try:
            run = self.analysis.cancel(
                principal,
                run_id=run_id,
                expected_version=value["expectedVersion"],
            )
            return ExecutionResult(
                {
                    "cancelAnalysis": {
                        "clientMutationId": value.get("clientMutationId"),
                        "run": self._run_node(run),
                    }
                }
            )
        except PreconditionFailed:
            return ExecutionResult(
                {
                    "cancelAnalysis": {
                        "clientMutationId": value.get("clientMutationId"),
                        "code": "PRECONDITION_FAILED",
                        "message": "Run version changed",
                        "field": "expectedVersion",
                    }
                }
            )
        except ConflictError:
            return ExecutionResult(
                {
                    "cancelAnalysis": {
                        "clientMutationId": value.get("clientMutationId"),
                        "code": "CONFLICT",
                        "message": "Run is already terminal",
                        "field": "runId",
                    }
                }
            )
        except KeyError:
            return ExecutionResult(
                {
                    "cancelAnalysis": {
                        "clientMutationId": value.get("clientMutationId"),
                        "code": "NOT_FOUND",
                        "message": "Run was not found",
                        "field": "runId",
                    }
                }
            )

    def _op_RunUpdates(
        self, variables: dict[str, Any], context: RequestContext
    ) -> ExecutionResult:
        principal = context.principal
        require_field(principal, "Subscription.analysisRunUpdated")
        type_name, run_id = decode_global_id(variables["runId"])
        if type_name != "AnalysisRun":
            raise ValidationError("runId has the wrong global identifier type")
        after = int(variables.get("afterSequence") or 0)
        source = [
            SubscriptionEvent(int(event["sequence"]), event)
            for event in self.analysis.updates(principal, run_id, after)
        ]
        delivered = ResumableSubscription().resume(source, after=after)
        return ExecutionResult(
            {
                "analysisRunUpdated": [
                    {
                        "sequence": str(event.sequence),
                        "occurredAt": "2026-08-08T12:00:00Z",
                        "run": self._run_node(event.payload["run"]),
                    }
                    for event in delivered
                ]
            }
        )

    def _op_NodeLookup(
        self, variables: dict[str, Any], context: RequestContext
    ) -> ExecutionResult:
        value = variables["by"]
        present = [key for key, item in value.items() if item is not None]
        if len(present) != 1:
            raise ValidationError(
                "NodeLookup requires exactly one non-null field"
            )

        if value.get("id"):
            type_name, local_id = decode_global_id(value["id"])
        else:
            resolved = self.analysis.resolve_external_id(
                context.principal, value["externalId"]
            )
            if resolved is not None:
                type_name, item = resolved
                local_id = item["id"]
            else:
                item = self.artifacts.resolve_external_id(
                    context.principal, value["externalId"]
                )
                if item is None:
                    return ExecutionResult({"node": None})
                type_name, local_id = "Artifact", item["id"]

        if type_name == "Project":
            require_field(context.principal, "Query.project")
            item = self.analysis.get_project(context.principal, local_id)
        elif type_name == "AnalysisRun":
            require_field(context.principal, "Query.analysisRun")
            item = self.analysis.get_run(context.principal, local_id)
        elif type_name == "Artifact":
            require_field(context.principal, "Query.artifact")
            item = self.artifacts.get(context.principal, local_id)
        else:
            raise ValidationError("unsupported node type")

        if item is None:
            return ExecutionResult({"node": None})
        return ExecutionResult(
            {
                "node": {
                    "__typename": type_name,
                    "id": encode_global_id(type_name, local_id),
                }
            }
        )
