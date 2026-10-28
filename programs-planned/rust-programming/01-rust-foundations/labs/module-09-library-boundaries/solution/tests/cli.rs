use std::process::Command;

fn registry() -> Command {
    Command::new(env!("CARGO_BIN_EXE_registry"))
}

#[test]
fn help_uses_stdout_and_success() {
    let output = registry().arg("help").output().expect("run registry");
    assert!(output.status.success());
    assert!(String::from_utf8(output.stdout).expect("UTF-8").contains("registry commands:"));
    assert!(output.stderr.is_empty());
}

#[test]
fn add_produces_deterministic_success_output() {
    let output = registry().args(["add", "record", "parser"]).output().expect("run registry");
    assert!(output.status.success());
    assert_eq!(String::from_utf8(output.stdout).expect("UTF-8"), "added 1: record parser\n");
    assert!(output.stderr.is_empty());
}

#[test]
fn parse_failure_uses_stderr_and_exit_two() {
    let output = registry().arg("unknown").output().expect("run registry");
    assert_eq!(output.status.code(), Some(2));
    assert!(output.stdout.is_empty());
    assert_eq!(
        String::from_utf8(output.stderr).expect("UTF-8"),
        "error: unknown command `unknown`\n"
    );
}
