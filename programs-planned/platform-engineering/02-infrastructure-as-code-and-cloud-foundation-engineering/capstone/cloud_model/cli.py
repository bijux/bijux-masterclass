from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .backup import create_manifest, materialize_backup, restore_backup
from .compute import validate_image_release, validate_launch_contract, replacement_capacity
from .cost_quota import evaluate_cost_profile, evaluate_quotas
from .drift import classify_difference
from .iam import evaluate_policy, validate_policy_shape
from .network import trace_path, validate_network_plan
from .organization import validate_organization
from .plan import build_plan, plan_summary
from .release import evaluate_candidate
from .state_backend import validate_backend_profile


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def emit(value: Any, output: Path | None) -> None:
    text = json.dumps(value, indent=2, sort_keys=True) + "\n"
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text, encoding="utf-8")
    print(text, end="")


def main() -> int:
    parser = argparse.ArgumentParser(description="Atlas Cloud Foundation semantic proof tool")
    sub = parser.add_subparsers(dest="command", required=True)

    plan_p = sub.add_parser("plan")
    plan_p.add_argument("config", type=Path)
    plan_p.add_argument("state", type=Path)
    plan_p.add_argument("--moves", type=Path)
    plan_p.add_argument("--output", type=Path)

    backend_p = sub.add_parser("backend-check")
    backend_p.add_argument("profile", type=Path)

    org_p = sub.add_parser("organization-check")
    org_p.add_argument("model", type=Path)

    net_p = sub.add_parser("network-check")
    net_p.add_argument("plan", type=Path)
    net_p.add_argument("--source-subnet")
    net_p.add_argument("--destination-ip")

    iam_p = sub.add_parser("iam-check")
    iam_p.add_argument("policy", type=Path)
    iam_p.add_argument("vectors", type=Path)

    compute_p = sub.add_parser("compute-check")
    compute_p.add_argument("image", type=Path)
    compute_p.add_argument("launch", type=Path)

    backup_p = sub.add_parser("backup-tour")
    backup_p.add_argument("source", type=Path)
    backup_p.add_argument("backup", type=Path)
    backup_p.add_argument("restore", type=Path)

    drift_p = sub.add_parser("drift-check")
    drift_p.add_argument("differences", type=Path)

    release_p = sub.add_parser("release-check")
    release_p.add_argument("candidate", type=Path)

    args = parser.parse_args()
    if args.command == "plan":
        moves = load(args.moves) if args.moves else None
        actions = build_plan(load(args.config)["resources"], load(args.state)["resources"], moves=moves)
        emit(plan_summary(actions), args.output)
        return 0
    if args.command == "backend-check":
        errors = validate_backend_profile(load(args.profile))
        emit({"valid": not errors, "errors": errors}, None)
        return 0 if not errors else 1
    if args.command == "organization-check":
        errors = validate_organization(load(args.model))
        emit({"valid": not errors, "errors": errors}, None)
        return 0 if not errors else 1
    if args.command == "network-check":
        plan = load(args.plan)
        errors = validate_network_plan(plan)
        result: dict[str, Any] = {"valid": not errors, "errors": errors}
        if args.source_subnet and args.destination_ip:
            result["path"] = trace_path(plan, source_subnet=args.source_subnet, destination_ip=args.destination_ip)
        emit(result, None)
        return 0 if not errors else 1
    if args.command == "iam-check":
        policy = load(args.policy)
        shape_errors = validate_policy_shape(policy)
        vector_results = []
        for vector in load(args.vectors):
            observed = evaluate_policy(policy, action=vector["action"], resource=vector["resource"], context=vector.get("context"))
            vector_results.append({**vector, "observed": observed["decision"], "passed": observed["decision"] == vector["expected"]})
        result = {"shapeErrors": shape_errors, "vectors": vector_results, "valid": not shape_errors and all(v["passed"] for v in vector_results)}
        emit(result, None)
        return 0 if result["valid"] else 1
    if args.command == "compute-check":
        image, launch = load(args.image), load(args.launch)
        errors = validate_image_release(image) + validate_launch_contract(launch, image)
        result = {"valid": not errors, "errors": errors, "replacementCapacity": replacement_capacity(current_instances=1, desired_instances=1, create_before_destroy=True, quota=int(launch.get("instanceQuota", 1)))}
        emit(result, None)
        return 0 if not errors else 1
    if args.command == "backup-tour":
        manifest = create_manifest(args.source, release="atlas-cloud-foundation-1.0", consistency_point="lab")
        materialize_backup(args.source, args.backup, manifest)
        result = restore_backup(args.backup, args.restore)
        emit(result, None)
        return 0
    if args.command == "drift-check":
        emit({"differences": [classify_difference(row) for row in load(args.differences)]}, None)
        return 0
    if args.command == "release-check":
        result = evaluate_candidate(load(args.candidate))
        emit(result, None)
        return 0 if result["decision"] in {"accept", "dependency-light-only", "review"} else 1
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
