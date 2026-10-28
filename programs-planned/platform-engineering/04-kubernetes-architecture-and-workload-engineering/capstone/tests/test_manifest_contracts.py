from pathlib import Path
import json
import yaml

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "manifests" / "base"
CTRL = ROOT / "manifests" / "controller"


def docs(path):
    return [d for d in yaml.safe_load_all(path.read_text()) if d]


def one(path):
    values = docs(path)
    assert len(values) == 1
    return values[0]


def test_release_images_match_predecessor():
    predecessor = json.loads((ROOT / "predecessor" / "image-release.json").read_text())
    expected = {f"{i['repository']}@{i['digest']}" for i in predecessor["images"]}
    actual = set()
    for name in ("10-api-deployment.yaml", "11-worker-deployment.yaml"):
        doc = one(BASE / name)
        actual.add(doc["spec"]["template"]["spec"]["containers"][0]["image"])
    assert actual == expected


def test_no_mutable_latest_tag_in_release_manifests():
    text = "\n".join(p.read_text() for p in BASE.glob("*.yaml"))
    assert ":latest" not in text


def test_api_selector_matches_template():
    doc = one(BASE / "10-api-deployment.yaml")
    selector = doc["spec"]["selector"]["matchLabels"]
    labels = doc["spec"]["template"]["metadata"]["labels"]
    assert all(labels[k] == v for k, v in selector.items())


def test_worker_selector_matches_template():
    doc = one(BASE / "11-worker-deployment.yaml")
    selector = doc["spec"]["selector"]["matchLabels"]
    labels = doc["spec"]["template"]["metadata"]["labels"]
    assert all(labels[k] == v for k, v in selector.items())


def test_api_availability_contract():
    doc = one(BASE / "10-api-deployment.yaml")
    assert doc["spec"]["replicas"] == 3
    assert doc["spec"]["strategy"]["rollingUpdate"] == {"maxSurge": 1, "maxUnavailable": 0}
    assert doc["spec"]["minReadySeconds"] == 10


def test_pdb_matches_api_population():
    pdb = one(BASE / "13-api-pdb.yaml")
    api = one(BASE / "10-api-deployment.yaml")
    assert pdb["spec"]["minAvailable"] == 2
    assert pdb["spec"]["selector"]["matchLabels"] == api["spec"]["selector"]["matchLabels"]


def test_worker_uses_pvc_for_inherited_durable_paths():
    doc = one(BASE / "11-worker-deployment.yaml")
    volumes = {v["name"]: v for v in doc["spec"]["template"]["spec"]["volumes"]}
    assert "persistentVolumeClaim" in volumes["spool"]
    assert "persistentVolumeClaim" in volumes["results"]


def test_service_selector_matches_api():
    service = one(BASE / "12-api-service.yaml")
    api = one(BASE / "10-api-deployment.yaml")
    assert service["spec"]["selector"] == api["spec"]["selector"]["matchLabels"]
    assert service["spec"]["ports"][0]["targetPort"] == "http"


def test_crd_is_structural_and_bounds_worker_scale():
    crd = one(CTRL / "00-crd.yaml")
    version = crd["spec"]["versions"][0]
    props = version["schema"]["openAPIV3Schema"]["properties"]["spec"]["properties"]
    assert props["apiImage"]["pattern"].endswith("{64}$")
    assert props["workerReplicas"]["maximum"] == 1
    assert version["subresources"] == {"status": {}}


def test_controller_role_is_namespaced_and_cannot_read_secrets():
    role = docs(CTRL / "01-rbac.yaml")[1]
    assert role["kind"] == "Role"
    resources = {resource for rule in role["rules"] for resource in rule["resources"]}
    assert "secrets" not in resources
    assert "nodes" not in resources


def test_kind_lane_is_explicitly_observational():
    doc = one(ROOT / "kind" / "observation-workload.yaml")
    assert doc["metadata"]["annotations"]["platform.bijux.dev/evidence-class"] == "local-observation-only"


def test_course_5_handoff_preserves_port_and_readiness():
    service = yaml.safe_load((ROOT / "handoff" / "service-connectivity.yaml").read_text())
    readiness = yaml.safe_load((ROOT / "handoff" / "readiness-and-endpoints.yaml").read_text())
    assert service["services"][0]["ports"][0]["port"] == 8080
    assert readiness["api"]["readinessPath"] == "/ready"
    assert readiness["api"]["remoteDependenciesInLiveness"] == "forbidden"
