use std::fs;
use std::process::Command;
use std::time::{SystemTime, UNIX_EPOCH};

fn fixture(contents: &str) -> std::path::PathBuf {
    let stamp = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap()
        .as_nanos();
    let path = std::env::temp_dir().join(format!("ledgerflow-{stamp}.tsv"));
    fs::write(&path, contents).unwrap();
    path
}

#[test]
fn summary_command_runs_as_a_real_process() {
    let path = fixture("LEDGERFLOW-V1\n1\ta\topen\t0\tstart\n");
    let output = Command::new(env!("CARGO_BIN_EXE_ledgerflow"))
        .args(["summary", path.to_str().unwrap()])
        .output()
        .unwrap();
    let _ = fs::remove_file(path);
    assert!(output.status.success());
    let stdout = String::from_utf8(output.stdout).unwrap();
    assert!(stdout.contains("events_accepted\t1"));
    assert!(stdout.contains("ACCOUNT\ta\topen\t0\t1"));
}

#[test]
fn data_failure_uses_exit_class_one_and_still_reports() {
    let path = fixture("LEDGERFLOW-V1\n1\ta\twithdraw\t1\tbad\n");
    let output = Command::new(env!("CARGO_BIN_EXE_ledgerflow"))
        .args(["check", path.to_str().unwrap()])
        .output()
        .unwrap();
    let _ = fs::remove_file(path);
    assert_eq!(output.status.code(), Some(1));
    let stdout = String::from_utf8(output.stdout).unwrap();
    assert!(stdout.contains("LF012"));
    assert!(stdout.contains("errors\t1"));
}

#[test]
fn missing_file_uses_exit_class_two() {
    let output = Command::new(env!("CARGO_BIN_EXE_ledgerflow"))
        .args(["check", "/definitely/not/a/ledgerflow/file"])
        .output()
        .unwrap();
    assert_eq!(output.status.code(), Some(2));
    assert!(String::from_utf8(output.stderr)
        .unwrap()
        .contains("cannot read"));
}
