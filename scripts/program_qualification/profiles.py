"""Name the representative PR contracts separately from exhaustive manual proof."""

from __future__ import annotations

SNAKEMAKE_FAST_TESTS = [
    "tests/test_fastqio.py",
    "tests/test_trim.py",
    "tests/test_kmer.py",
    "tests/test_dedup_fastq.py",
    "tests/test_discover_samples.py",
    "tests/test_provenance_helpers.py",
    "tests/test_verify_consumer_contract.py",
    "tests/test_verify_publish_script.py",
    "tests/test_publish_compatibility_audit.py",
    "tests/test_software_boundary_audit.py",
    "tests/test_scheduler_policy_audit.py",
    "tests/test_file_contract_audit.py::test_declared_policy_must_be_an_input",
    "tests/test_workflow_integration.py",
]

DVC_FAST_TESTS = [
    "tests/test_prepare.py",
    "tests/test_model.py",
    "tests/test_verify.py",
    "tests/test_bundle_manifest.py",
    "tests/test_inspect.py",
]

FUNCTIONAL_FAST_TESTS = [
    "tests/unit/result/",
    "tests/unit/boundaries/",
    "tests/unit/pipelines/",
    "tests/unit/policies/",
    "tests/unit/rag/test_api.py",
    "tests/unit/rag/test_stages.py",
    "tests/learning/test_module_10_retrieval.py",
]

FAST_TESTS = {
    "reproducible-research/deep-dive-snakemake": SNAKEMAKE_FAST_TESTS,
    "reproducible-research/deep-dive-dvc": DVC_FAST_TESTS,
    "python-programming/python-functional-programming": FUNCTIONAL_FAST_TESTS,
}

# Full qualification retains the existing published command and its assertions,
# clean-room execution, complete pytest collection and audit selftests.
FULL_COMMANDS = {
    "reproducible-research/deep-dive-snakemake": [
        "make",
        "-C",
        "programs/reproducible-research/deep-dive-snakemake/capstone",
        "bootstrap-confirm",
    ],
}
