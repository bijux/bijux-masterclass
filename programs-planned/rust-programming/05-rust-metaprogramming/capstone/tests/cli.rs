use std::process::Command;

fn binary() -> Command { Command::new(env!("CARGO_BIN_EXE_commandforge")) }

#[test]
fn list_is_stable() {
    let output = binary().arg("list").output().expect("run commandforge");
    assert!(output.status.success());
    let stdout = String::from_utf8(output.stdout).unwrap();
    let names = stdout.lines().map(|line| line.split_whitespace().next().unwrap()).collect::<Vec<_>>();
    assert_eq!(names, vec!["add", "slug", "repeat", "contains"]);
}

#[test]
fn command_failure_uses_generated_exit_code() {
    let output = binary().args(["run", "repeat", "--text", "x", "--times", "0"]).output().expect("run commandforge");
    assert_eq!(output.status.code(), Some(1));
    assert!(String::from_utf8(output.stderr).unwrap().contains("between 1 and 20"));
}

#[test]
fn usage_failure_is_distinct() {
    let output = binary().args(["explain"]).output().expect("run commandforge");
    assert_eq!(output.status.code(), Some(2));
}
