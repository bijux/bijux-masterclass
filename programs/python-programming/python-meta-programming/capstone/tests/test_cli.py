from __future__ import annotations

import json

from incident_plugins.cli import main


def test_manifest_command_renders_public_runtime_shape(capsys) -> None:
    exit_code = main(["manifest", "--group", "delivery"])

    captured = json.loads(capsys.readouterr().out)

    assert exit_code == 0
    assert [item["plugin_name"] for item in captured["delivery"]] == [
        "console",
        "pager",
        "webhook",
    ]


def test_signatures_command_renders_generated_constructor_and_action_shapes(capsys) -> None:
    exit_code = main(["signatures", "--group", "delivery"])

    captured = json.loads(capsys.readouterr().out)

    assert exit_code == 0
    console = captured["delivery"][0]
    assert console["plugin_name"] == "console"
    assert console["constructor"] == "(*, prefix='[incident]', stream='stdout', uppercase_severity=False)"
    assert console["actions"]["deliver"] == "(self, *, title: 'str', severity: 'str', summary: 'str') -> 'str'"


def test_plugin_command_renders_one_concrete_plugin_contract(capsys) -> None:
    exit_code = main(["plugin", "delivery", "webhook"])

    captured = json.loads(capsys.readouterr().out)

    assert exit_code == 0
    assert captured["plugin_name"] == "webhook"
    assert captured["fields"][0]["name"] == "endpoint"
    assert captured["actions"][0]["name"] == "deliver"


def test_field_command_renders_one_concrete_field_contract(capsys) -> None:
    exit_code = main(["field", "delivery", "webhook", "endpoint"])

    captured = json.loads(capsys.readouterr().out)

    assert exit_code == 0
    assert captured["plugin_name"] == "webhook"
    assert captured["field"]["name"] == "endpoint"
    assert captured["field"]["kind"] == "string"
    assert captured["field"]["minimum"] == 8


def test_action_command_renders_one_concrete_action_contract(capsys) -> None:
    exit_code = main(["action", "delivery", "pager", "preview"])

    captured = json.loads(capsys.readouterr().out)

    assert exit_code == 0
    assert captured["plugin_name"] == "pager"
    assert captured["action"]["name"] == "preview"
    assert captured["action"]["returns"] == "str"
    assert captured["action"]["signature"] == "(self, *, title: 'str', severity: 'str', summary: 'str') -> 'str'"


def test_bind_action_command_validates_arguments_without_execution(capsys) -> None:
    exit_code = main(
        [
            "bind-action",
            "delivery",
            "console",
            "deliver",
            "--arg",
            "title=CPU high",
            "--arg",
            "severity=warning",
            "--arg",
            "summary=node-1 crossed 90%",
        ]
    )

    captured = json.loads(capsys.readouterr().out)

    assert exit_code == 0
    assert captured == {
        "group": "delivery",
        "plugin_name": "console",
        "action_name": "deliver",
        "bound_arguments": {
            "title": "CPU high",
            "severity": "warning",
            "summary": "node-1 crossed 90%",
        },
        "executed": False,
    }


def test_action_wrapper_command_exposes_logical_and_shell_signatures(capsys) -> None:
    exit_code = main(
        [
            "action-wrapper",
            "delivery",
            "console",
            "deliver",
        ]
    )

    captured = json.loads(capsys.readouterr().out)

    assert exit_code == 0
    assert captured["constructed"] is False
    assert captured["executed"] is False
    assert captured["wrapper"]["wrapper_depth"] == 1
    assert captured["wrapper"]["visible_signature"] == (
        "(self, *, title: 'str', severity: 'str', summary: 'str') -> 'str'"
    )
    assert captured["wrapper"]["chain"][0]["owns_action_spec"] is True
    assert captured["wrapper"]["chain"][0]["owns_explicit_signature"] is True
    assert captured["wrapper"]["chain"][1]["owns_action_spec"] is False
    assert captured["wrapper"]["chain"][1]["owns_explicit_signature"] is False
    assert captured["wrapper"]["action_spec_signature_matches_original"] is True


def test_check_action_command_reports_annotation_contract_without_execution(capsys) -> None:
    exit_code = main(
        [
            "check-action",
            "delivery",
            "console",
            "deliver",
            "--arg",
            "title=CPU high",
            "--arg",
            "severity=warning",
            "--arg",
            "summary=node-1 crossed 90%",
        ]
    )

    captured = json.loads(capsys.readouterr().out)

    assert exit_code == 0
    assert captured["accepted"] is True
    assert captured["contract_complete"] is True
    assert [item["name"] for item in captured["checked"]] == [
        "title",
        "severity",
        "summary",
    ]
    assert captured["refused"] == []
    assert captured["unchecked"] == []
    assert captured["policy"]["scope"] == "arguments-only"
    assert captured["policy"]["return_checked"] is False
    assert captured["constructed"] is False
    assert captured["executed"] is False


def test_invoke_command_runs_a_plugin_action(capsys) -> None:
    exit_code = main(
        [
            "invoke",
            "delivery",
            "console",
            "deliver",
            "--config",
            "prefix=[ops]",
            "--config",
            "uppercase_severity=true",
            "--arg",
            "title=CPU high",
            "--arg",
            "severity=warning",
            "--arg",
            "summary=node-1 crossed 90%",
        ]
    )

    captured = json.loads(capsys.readouterr().out)

    assert exit_code == 0
    assert captured["result"] == "[ops] WARNING CPU high: node-1 crossed 90%"


def test_trace_command_exposes_configuration_and_action_history(capsys) -> None:
    exit_code = main(
        [
            "trace",
            "delivery",
            "pager",
            "preview",
            "--config",
            "service=core",
            "--config",
            "routing_key=sev1",
            "--arg",
            "title=Queue lag",
            "--arg",
            "severity=critical",
            "--arg",
            "summary=worker backlog growing",
        ]
    )

    captured = json.loads(capsys.readouterr().out)

    assert exit_code == 0
    assert captured["configuration"]["service"] == "core"
    assert captured["history"][-1]["action"] == "preview"
