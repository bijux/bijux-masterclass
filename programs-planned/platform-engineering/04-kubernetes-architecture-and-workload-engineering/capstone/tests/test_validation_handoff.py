from pathlib import Path
import json
from atlas_kube.validation import validate_tree, load_documents, validate_document
from atlas_kube.handoff import verify_manifest

ROOT=Path(__file__).resolve().parents[1]


def test_base_manifests_pass_policy():
    assert validate_tree(ROOT/"manifests"/"base")==[]


def test_controller_workload_manifests_pass_policy():
    findings=validate_tree(ROOT/"manifests"/"controller")
    assert findings==[]


def test_mutable_image_rejected():
    path=ROOT/"planted-defects"/"KUBE-01-mutable-image"/"workload.yaml"
    doc=load_documents(path)[0]
    assert any("not digest pinned" in x for x in validate_document(doc))


def test_root_runtime_rejected():
    path=ROOT/"planted-defects"/"KUBE-02-root-runtime"/"workload.yaml"
    errors=validate_document(load_documents(path)[0])
    assert any("runAsNonRoot" in x for x in errors)
    assert any("privilege escalation" in x for x in errors)


def test_selector_mismatch_rejected():
    path=ROOT/"planted-defects"/"KUBE-03-selector-mismatch"/"workload.yaml"
    assert any("selector label" in x for x in validate_document(load_documents(path)[0]))


def test_handoff_manifest(): assert verify_manifest(ROOT/"handoff")==[]


def test_predecessor_manifest_exact(): assert verify_manifest(ROOT/"predecessor")==[]


def test_release_states():
    states={json.loads(p.read_text())["decision"] for p in (ROOT/"releases").glob("*/release.json")}
    assert {"accepted","rejected","review-required","not-executed"} <= states
