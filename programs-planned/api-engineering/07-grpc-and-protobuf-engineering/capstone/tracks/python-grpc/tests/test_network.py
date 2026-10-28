from __future__ import annotations

from hashlib import sha256
import unittest
import grpc

from analysis_rpc import analysis_pb2, analysis_pb2_grpc
from analysis_rpc.client import AnalysisClient
from analysis_rpc.models import State
from analysis_rpc.server import start_server


class LiveGrpcTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.server, cls.store, cls.port = start_server()
        cls.channel = grpc.insecure_channel(f"127.0.0.1:{cls.port}")
        cls.client = AnalysisClient(cls.channel, "learner-write")

    @classmethod
    def tearDownClass(cls) -> None:
        cls.channel.close()
        cls.server.stop(grace=0).wait()

    def test_create_get_and_idempotent_replay(self) -> None:
        first = self.client.create_run(
            parent="projects/p-1", request_id="network-create-1",
            dataset_name="datasets/d-1", algorithm="qc",
        )
        replay = self.client.create_run(
            parent="projects/p-1", request_id="network-create-1",
            dataset_name="datasets/d-1", algorithm="qc",
        )
        self.assertEqual(first.name, replay.name)
        self.assertEqual(self.client.get_run(first.name).name, first.name)

    def test_changed_input_returns_already_exists(self) -> None:
        self.client.create_run(
            parent="projects/p-1", request_id="network-conflict-1",
            dataset_name="datasets/d-1", algorithm="qc",
        )
        with self.assertRaises(grpc.RpcError) as caught:
            self.client.create_run(
                parent="projects/p-1", request_id="network-conflict-1",
                dataset_name="datasets/d-2", algorithm="qc",
            )
        self.assertEqual(caught.exception.code(), grpc.StatusCode.ALREADY_EXISTS)

    def test_invalid_algorithm_returns_invalid_argument(self) -> None:
        with self.assertRaises(grpc.RpcError) as caught:
            self.client.create_run(
                parent="projects/p-1", request_id="network-invalid-1",
                dataset_name="datasets/d-1", algorithm="unknown",
            )
        self.assertEqual(caught.exception.code(), grpc.StatusCode.INVALID_ARGUMENT)

    def test_wrong_scope_returns_permission_denied(self) -> None:
        read_client = AnalysisClient(self.channel, "learner-read")
        with self.assertRaises(grpc.RpcError) as caught:
            read_client.create_run(
                parent="projects/p-1", request_id="network-denied-1",
                dataset_name="datasets/d-1", algorithm="qc",
            )
        self.assertEqual(caught.exception.code(), grpc.StatusCode.PERMISSION_DENIED)

    def test_watch_resume(self) -> None:
        run = self.client.create_run(
            parent="projects/p-1", request_id="network-watch-1",
            dataset_name="datasets/d-1", algorithm="qc",
        )
        self.store.advance_run(run.name, state=State.RUNNING, progress=10)
        events = list(self.client.watch_run(run.name, after=1))
        self.assertEqual([event.sequence for event in events], [2])

    def test_client_stream_upload(self) -> None:
        body = b"streamed-dataset"
        response = self.client.upload(body, request_id="network-upload-1")
        self.assertEqual(response.size_bytes, len(body))
        self.assertEqual(response.sha256, sha256(body).hexdigest())

    def test_server_stream_download(self) -> None:
        self.assertEqual(self.client.download(), b"analysis-artifact\n")

    def test_worker_stream_requires_hello(self) -> None:
        stub = analysis_pb2_grpc.WorkerPlaneServiceStub(self.channel)
        def frames():
            yield analysis_pb2.WorkerToControl(
                ready=analysis_pb2.WorkerReady(
                    worker_id="worker-1", available_slots=1
                )
            )
        with self.assertRaises(grpc.RpcError) as caught:
            list(stub.Work(
                frames(),
                metadata=(("authorization", "Bearer worker-1"),),
                timeout=2,
            ))
        self.assertEqual(caught.exception.code(), grpc.StatusCode.INVALID_ARGUMENT)


if __name__ == "__main__":
    unittest.main()
