from __future__ import annotations
from . import analysis_pb2
from .models import Event, Run

def run_to_proto(run: Run) -> analysis_pb2.AnalysisRun:
    message = analysis_pb2.AnalysisRun(
        name=run.name,
        project_name=run.project_name,
        dataset_name=run.dataset_name,
        state=int(run.state),
        progress_percent=run.progress_percent,
        etag=run.etag,
        revision=run.revision,
    )
    if run.result_summary is not None:
        message.result_summary = run.result_summary
    if run.failure_code is not None:
        message.failure_code = run.failure_code
    return message

def event_to_proto(event: Event) -> analysis_pb2.RunEvent:
    return analysis_pb2.RunEvent(
        event_id=event.event_id,
        run_name=event.run_name,
        sequence=event.sequence,
        snapshot=run_to_proto(event.snapshot),
        type=event.type,
    )
