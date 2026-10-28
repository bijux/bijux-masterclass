from __future__ import annotations
from dataclasses import dataclass
from hashlib import sha256
from typing import Iterable
import grpc

from . import analysis_pb2, analysis_pb2_grpc
from .status import safe_error


@dataclass
class AnalysisClient:
    channel: grpc.Channel
    token: str

    def __post_init__(self) -> None:
        self.control = analysis_pb2_grpc.AnalysisControlServiceStub(self.channel)
        self.transfer = analysis_pb2_grpc.DatasetTransferServiceStub(self.channel)
        self.worker = analysis_pb2_grpc.WorkerPlaneServiceStub(self.channel)

    @property
    def metadata(self):
        return (("authorization", f"Bearer {self.token}"),)

    def create_run(
        self,
        *,
        parent: str,
        request_id: str,
        dataset_name: str,
        algorithm: str,
        timeout: float = 2.0,
    ):
        return self.control.CreateRun(
            analysis_pb2.CreateRunRequest(
                parent=parent,
                request_id=request_id,
                dataset_name=dataset_name,
                algorithm=algorithm,
            ),
            metadata=self.metadata,
            timeout=timeout,
        )

    def get_run(self, name: str, *, timeout: float = 2.0):
        return self.control.GetRun(
            analysis_pb2.GetRunRequest(name=name),
            metadata=self.metadata,
            timeout=timeout,
        )

    def cancel_run(
        self,
        name: str,
        etag: str,
        request_id: str,
        *,
        timeout: float = 2.0,
    ):
        return self.control.CancelRun(
            analysis_pb2.CancelRunRequest(
                name=name, etag=etag, request_id=request_id
            ),
            metadata=self.metadata,
            timeout=timeout,
        )

    def watch_run(self, name: str, after: int = 0, *, timeout: float = 2.0):
        return self.control.WatchRun(
            analysis_pb2.WatchRunRequest(
                name=name, resume_after_sequence=after
            ),
            metadata=self.metadata,
            timeout=timeout,
        )

    def upload(self, body: bytes, *, request_id: str = "upload-1"):
        digest = sha256(body).hexdigest()
        def frames():
            yield analysis_pb2.UploadDatasetRequest(
                metadata=analysis_pb2.UploadMetadata(
                    parent="projects/p-1",
                    request_id=request_id,
                    filename="dataset.bin",
                    media_type="application/octet-stream",
                    sha256=digest,
                    expected_size_bytes=len(body),
                )
            )
            for offset in range(0, len(body), 8):
                yield analysis_pb2.UploadDatasetRequest(
                    chunk=body[offset:offset + 8]
                )
        return self.transfer.UploadDataset(
            frames(), metadata=self.metadata, timeout=2.0
        )

    def download(self, name: str = "artifacts/a-1") -> bytes:
        chunks = list(self.transfer.DownloadArtifact(
            analysis_pb2.DownloadArtifactRequest(name=name),
            metadata=self.metadata,
            timeout=2.0,
        ))
        body = b"".join(chunk.data for chunk in chunks)
        if not chunks or not chunks[-1].complete:
            raise RuntimeError("incomplete artifact stream")
        if sha256(body).hexdigest() != chunks[-1].sha256:
            raise RuntimeError("artifact checksum mismatch")
        return body


def describe_rpc_error(error: grpc.RpcError) -> dict[str, object]:
    return safe_error(error.code(), error.details(), error.trailing_metadata())
