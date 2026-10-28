#!/usr/bin/env python3
"""Rebuild the checked generated-equivalent Python message module."""
from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
descriptor = (ROOT / "capstone/contracts/descriptors/analysis-v1.pb").read_bytes()
target = ROOT / "capstone/tracks/python-grpc/src/analysis_rpc/analysis_pb2.py"
body = (
    "# Generated-equivalent educational artifact.\n"
    "from google.protobuf import descriptor_pool as _descriptor_pool\n"
    "from google.protobuf.internal import builder as _builder\n\n"
    f"DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile({descriptor!r})\n"
    "_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())\n"
    "_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, __name__, globals())\n"
)
target.write_text(body)
print(target)
