from __future__ import annotations

from concurrent import futures
from hashlib import sha256
import time
import grpc

from . import analysis_pb2, analysis_pb2_grpc
from .errors import RpcApplicationError, PermissionDenied
from .mapping import event_to_proto, run_to_proto
from .security import authenticate, require, require_tenant
from .status import abort_for
from .store import InMemoryAnalysisStore
from .streaming import chunk_bytes, parse_upload


class AnalysisControlService(analysis_pb2_grpc.AnalysisControlServiceServicer):
    def __init__(self, store: InMemoryAnalysisStore) -> None:
        self.store = store

    def CreateRun(self, request, context):
        try:
            principal = authenticate(context.invocation_metadata())
            require(principal, "runs:write")
            require_tenant(principal, request.parent)
            run = self.store.create_run(
                parent=request.parent,
                request_id=request.request_id,
                dataset_name=request.dataset_name,
                algorithm=request.algorithm,
                principal=principal,
            )
            return run_to_proto(run)
        except RpcApplicationError as error:
            abort_for(context, error)

    def GetRun(self, request, context):
        try:
            principal = authenticate(context.invocation_metadata())
            require(principal, "runs:read")
            run = self.store.get_run(request.name, principal)
            return run_to_proto(run)
        except RpcApplicationError as error:
            abort_for(context, error)

    def CancelRun(self, request, context):
        try:
            principal = authenticate(context.invocation_metadata())
            require(principal, "runs:write")
            run = self.store.cancel_run(
                name=request.name,
                etag=request.etag,
                request_id=request.request_id,
                principal=principal,
            )
            return run_to_proto(run)
        except RpcApplicationError as error:
            abort_for(context, error)

    def WatchRun(self, request, context):
        try:
            principal = authenticate(context.invocation_metadata())
            require(principal, "runs:read")
            for event in self.store.watch(
                request.name,
                int(request.resume_after_sequence),
                principal,
            ):
                if not context.is_active():
                    return
                yield event_to_proto(event)
        except RpcApplicationError as error:
            abort_for(context, error)


class DatasetTransferService(analysis_pb2_grpc.DatasetTransferServiceServicer):
    def __init__(self, store: InMemoryAnalysisStore) -> None:
        self.store = store

    def UploadDataset(self, request_iterator, context):
        try:
            principal = authenticate(context.invocation_metadata())
            require(principal, "datasets:write")
            parsed = parse_upload(request_iterator)
            require_tenant(principal, parsed.parent)
            name, size, digest = self.store.upload(
                parent=parsed.parent,
                request_id=parsed.request_id,
                filename=parsed.filename,
                expected_sha256=parsed.expected_sha256,
                expected_size=parsed.expected_size,
                chunks=parsed.chunks,
                max_bytes=2 * 1024 * 1024,
            )
            return analysis_pb2.UploadDatasetResponse(
                dataset_name=name,
                size_bytes=size,
                sha256=digest,
            )
        except RpcApplicationError as error:
            abort_for(context, error)

    def DownloadArtifact(self, request, context):
        try:
            principal = authenticate(context.invocation_metadata())
            require(principal, "artifacts:read")
            if principal.tenant != "tenant-a":
                raise PermissionDenied("permission denied")
            body, digest = self.store.download(
                request.name,
                offset=int(request.offset),
                limit=int(request.limit),
            )
            base_offset = int(request.offset)
            for offset, data, complete in chunk_bytes(body):
                if not context.is_active():
                    return
                yield analysis_pb2.ArtifactChunk(
                    offset=base_offset + offset,
                    data=data,
                    complete=complete,
                    sha256=digest if complete else "",
                )
        except RpcApplicationError as error:
            abort_for(context, error)


class WorkerPlaneService(analysis_pb2_grpc.WorkerPlaneServiceServicer):
    def __init__(self, store: InMemoryAnalysisStore) -> None:
        self.store = store

    def Work(self, request_iterator, context):
        try:
            principal = authenticate(context.invocation_metadata())
            require(principal, "worker:connect")
            iterator = iter(request_iterator)
            first = next(iterator, None)
            if first is None or first.WhichOneof("payload") != "hello":
                context.abort(
                    grpc.StatusCode.INVALID_ARGUMENT,
                    "first worker frame must be hello",
                )
            hello = first.hello
            if hello.worker_id != principal.subject:
                raise PermissionDenied("permission denied")
            if hello.tenant_id != principal.tenant:
                raise PermissionDenied("permission denied")
            yield analysis_pb2.ControlToWorker(heartbeat_interval_ms=5000)

            assignment = self.store.assign(
                hello.worker_id,
                hello.tenant_id,
                hello.max_concurrency,
            )
            if assignment is not None:
                yield analysis_pb2.ControlToWorker(
                    assignment=analysis_pb2.WorkAssignment(
                        assignment_id=assignment.assignment_id,
                        run_name=assignment.run_name,
                        algorithm=assignment.algorithm,
                        dataset_name=assignment.dataset_name,
                        lease_expires_unix_ms=assignment.lease_expires_unix_ms,
                        lease_generation=assignment.lease_generation,
                    )
                )

            for frame in iterator:
                if not context.is_active():
                    return
                kind = frame.WhichOneof("payload")
                if kind == "result":
                    result = frame.result
                    self.store.complete_assignment(
                        assignment_id=result.assignment_id,
                        worker_id=hello.worker_id,
                        generation=int(result.lease_generation),
                        success=result.success,
                        result_summary=result.result_summary,
                        failure_code=result.failure_code,
                    )
                elif kind not in {"ready", "progress"}:
                    context.abort(
                        grpc.StatusCode.INVALID_ARGUMENT,
                        "illegal worker frame",
                    )
        except RpcApplicationError as error:
            abort_for(context, error)


def create_server(
    *,
    store: InMemoryAnalysisStore | None = None,
    max_workers: int = 8,
) -> tuple[grpc.Server, InMemoryAnalysisStore]:
    store = store or InMemoryAnalysisStore()
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=max_workers),
        options=(
            ("grpc.max_receive_message_length", 3 * 1024 * 1024),
            ("grpc.max_send_message_length", 3 * 1024 * 1024),
        ),
    )
    analysis_pb2_grpc.add_AnalysisControlServiceServicer_to_server(
        AnalysisControlService(store), server
    )
    analysis_pb2_grpc.add_DatasetTransferServiceServicer_to_server(
        DatasetTransferService(store), server
    )
    analysis_pb2_grpc.add_WorkerPlaneServiceServicer_to_server(
        WorkerPlaneService(store), server
    )
    return server, store


def start_server(address: str = "127.0.0.1:0"):
    server, store = create_server()
    port = server.add_insecure_port(address)
    if port == 0:
        raise RuntimeError(f"could not bind {address}")
    server.start()
    return server, store, port


if __name__ == "__main__":
    server, _store, port = start_server()
    print(f"Analysis RPC listening on 127.0.0.1:{port}", flush=True)
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        server.stop(grace=2).wait()
