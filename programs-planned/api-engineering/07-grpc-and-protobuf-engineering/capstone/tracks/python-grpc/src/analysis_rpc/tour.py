from __future__ import annotations
import json
import grpc
from .client import AnalysisClient
from .server import start_server
from .models import State

def run_tour() -> dict[str, object]:
    server, store, port = start_server()
    channel = grpc.insecure_channel(f"127.0.0.1:{port}")
    client = AnalysisClient(channel, "learner-write")
    try:
        created = client.create_run(
            parent="projects/p-1",
            request_id="tour-create-1",
            dataset_name="datasets/d-1",
            algorithm="qc",
        )
        replay = client.create_run(
            parent="projects/p-1",
            request_id="tour-create-1",
            dataset_name="datasets/d-1",
            algorithm="qc",
        )
        store.advance_run(
            created.name,
            state=State.RUNNING,
            progress=50,
        )
        events = list(client.watch_run(created.name, after=1))
        uploaded = client.upload(b"course-seven")
        artifact = client.download()
        return {
            "created": created.name,
            "idempotent_replay": replay.name == created.name,
            "watch_sequences": [event.sequence for event in events],
            "uploaded_dataset": uploaded.dataset_name,
            "artifact_sha256_ok": len(artifact) > 0,
        }
    finally:
        channel.close()
        server.stop(grace=0).wait()

if __name__ == "__main__":
    print(json.dumps(run_tour(), indent=2, sort_keys=True))
