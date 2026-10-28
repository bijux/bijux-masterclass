use std::fs;
use std::process::Command;
use std::time::{SystemTime, UNIX_EPOCH};

fn temporary_manifest(contents: &str) -> std::path::PathBuf {
    let nonce = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .expect("clock after epoch")
        .as_nanos();
    let path = std::env::temp_dir().join(format!(
        "batchweave-{}-{nonce}.tsv",
        std::process::id()
    ));
    fs::write(&path, contents).expect("write fixture");
    path
}

#[test]
fn run_command_emits_stable_input_order() {
    let path = temporary_manifest(
        "BATCHWEAVE-V1\nslow\tprime-count\t60000\nfast\tword-count\tone two three\n",
    );
    let output = Command::new(env!("CARGO_BIN_EXE_batchweave"))
        .args([
            "run",
            path.to_str().expect("UTF-8 temp path"),
            "--workers",
            "2",
            "--queue-capacity",
            "1",
        ])
        .output()
        .expect("run binary");
    let _ = fs::remove_file(path);
    assert!(output.status.success());
    let stdout = String::from_utf8(output.stdout).expect("UTF-8 output");
    let slow = stdout.find("0\tslow").expect("slow row");
    let fast = stdout.find("1\tfast").expect("fast row");
    assert!(slow < fast);
}

#[test]
fn domain_failure_uses_product_exit_status_one() {
    let path = temporary_manifest("BATCHWEAVE-V1\nbad\tsort-integers\t1,nope\n");
    let output = Command::new(env!("CARGO_BIN_EXE_batchweave"))
        .args(["run", path.to_str().expect("UTF-8 temp path")])
        .output()
        .expect("run binary");
    let _ = fs::remove_file(path);
    assert_eq!(output.status.code(), Some(1));
    let stdout = String::from_utf8(output.stdout).expect("UTF-8 output");
    assert!(stdout.contains("failed"));
}

#[test]
fn malformed_input_uses_exit_status_two() {
    let path = temporary_manifest("WRONG\n");
    let output = Command::new(env!("CARGO_BIN_EXE_batchweave"))
        .args(["run", path.to_str().expect("UTF-8 temp path")])
        .output()
        .expect("run binary");
    let _ = fs::remove_file(path);
    assert_eq!(output.status.code(), Some(2));
    let stderr = String::from_utf8(output.stderr).expect("UTF-8 error");
    assert!(stderr.contains("expected BATCHWEAVE-V1"));
}
