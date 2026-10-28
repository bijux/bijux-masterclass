# Generated-equivalent gRPC bindings for the educational baseline.
import grpc
from . import analysis_pb2 as analysis__pb2


class AnalysisControlServiceStub:
    def __init__(self, channel):
        self.CreateRun = channel.unary_unary(
            "/bijux.analysis.v1.AnalysisControlService/CreateRun",
            request_serializer=analysis__pb2.CreateRunRequest.SerializeToString,
            response_deserializer=analysis__pb2.AnalysisRun.FromString,
        )
        self.GetRun = channel.unary_unary(
            "/bijux.analysis.v1.AnalysisControlService/GetRun",
            request_serializer=analysis__pb2.GetRunRequest.SerializeToString,
            response_deserializer=analysis__pb2.AnalysisRun.FromString,
        )
        self.CancelRun = channel.unary_unary(
            "/bijux.analysis.v1.AnalysisControlService/CancelRun",
            request_serializer=analysis__pb2.CancelRunRequest.SerializeToString,
            response_deserializer=analysis__pb2.AnalysisRun.FromString,
        )
        self.WatchRun = channel.unary_stream(
            "/bijux.analysis.v1.AnalysisControlService/WatchRun",
            request_serializer=analysis__pb2.WatchRunRequest.SerializeToString,
            response_deserializer=analysis__pb2.RunEvent.FromString,
        )


class AnalysisControlServiceServicer:
    def CreateRun(self, request, context):
        context.abort(grpc.StatusCode.UNIMPLEMENTED, "Method not implemented")
    def GetRun(self, request, context):
        context.abort(grpc.StatusCode.UNIMPLEMENTED, "Method not implemented")
    def CancelRun(self, request, context):
        context.abort(grpc.StatusCode.UNIMPLEMENTED, "Method not implemented")
    def WatchRun(self, request, context):
        context.abort(grpc.StatusCode.UNIMPLEMENTED, "Method not implemented")


def add_AnalysisControlServiceServicer_to_server(servicer, server):
    handlers = {
        "CreateRun": grpc.unary_unary_rpc_method_handler(
            servicer.CreateRun,
            request_deserializer=analysis__pb2.CreateRunRequest.FromString,
            response_serializer=analysis__pb2.AnalysisRun.SerializeToString,
        ),
        "GetRun": grpc.unary_unary_rpc_method_handler(
            servicer.GetRun,
            request_deserializer=analysis__pb2.GetRunRequest.FromString,
            response_serializer=analysis__pb2.AnalysisRun.SerializeToString,
        ),
        "CancelRun": grpc.unary_unary_rpc_method_handler(
            servicer.CancelRun,
            request_deserializer=analysis__pb2.CancelRunRequest.FromString,
            response_serializer=analysis__pb2.AnalysisRun.SerializeToString,
        ),
        "WatchRun": grpc.unary_stream_rpc_method_handler(
            servicer.WatchRun,
            request_deserializer=analysis__pb2.WatchRunRequest.FromString,
            response_serializer=analysis__pb2.RunEvent.SerializeToString,
        ),
    }
    server.add_generic_rpc_handlers((
        grpc.method_handlers_generic_handler(
            "bijux.analysis.v1.AnalysisControlService", handlers
        ),
    ))


class DatasetTransferServiceStub:
    def __init__(self, channel):
        self.UploadDataset = channel.stream_unary(
            "/bijux.analysis.v1.DatasetTransferService/UploadDataset",
            request_serializer=analysis__pb2.UploadDatasetRequest.SerializeToString,
            response_deserializer=analysis__pb2.UploadDatasetResponse.FromString,
        )
        self.DownloadArtifact = channel.unary_stream(
            "/bijux.analysis.v1.DatasetTransferService/DownloadArtifact",
            request_serializer=analysis__pb2.DownloadArtifactRequest.SerializeToString,
            response_deserializer=analysis__pb2.ArtifactChunk.FromString,
        )


class DatasetTransferServiceServicer:
    def UploadDataset(self, request_iterator, context):
        context.abort(grpc.StatusCode.UNIMPLEMENTED, "Method not implemented")
    def DownloadArtifact(self, request, context):
        context.abort(grpc.StatusCode.UNIMPLEMENTED, "Method not implemented")


def add_DatasetTransferServiceServicer_to_server(servicer, server):
    handlers = {
        "UploadDataset": grpc.stream_unary_rpc_method_handler(
            servicer.UploadDataset,
            request_deserializer=analysis__pb2.UploadDatasetRequest.FromString,
            response_serializer=analysis__pb2.UploadDatasetResponse.SerializeToString,
        ),
        "DownloadArtifact": grpc.unary_stream_rpc_method_handler(
            servicer.DownloadArtifact,
            request_deserializer=analysis__pb2.DownloadArtifactRequest.FromString,
            response_serializer=analysis__pb2.ArtifactChunk.SerializeToString,
        ),
    }
    server.add_generic_rpc_handlers((
        grpc.method_handlers_generic_handler(
            "bijux.analysis.v1.DatasetTransferService", handlers
        ),
    ))


class WorkerPlaneServiceStub:
    def __init__(self, channel):
        self.Work = channel.stream_stream(
            "/bijux.analysis.v1.WorkerPlaneService/Work",
            request_serializer=analysis__pb2.WorkerToControl.SerializeToString,
            response_deserializer=analysis__pb2.ControlToWorker.FromString,
        )


class WorkerPlaneServiceServicer:
    def Work(self, request_iterator, context):
        context.abort(grpc.StatusCode.UNIMPLEMENTED, "Method not implemented")


def add_WorkerPlaneServiceServicer_to_server(servicer, server):
    handlers = {
        "Work": grpc.stream_stream_rpc_method_handler(
            servicer.Work,
            request_deserializer=analysis__pb2.WorkerToControl.FromString,
            response_serializer=analysis__pb2.ControlToWorker.SerializeToString,
        )
    }
    server.add_generic_rpc_handlers((
        grpc.method_handlers_generic_handler(
            "bijux.analysis.v1.WorkerPlaneService", handlers
        ),
    ))
