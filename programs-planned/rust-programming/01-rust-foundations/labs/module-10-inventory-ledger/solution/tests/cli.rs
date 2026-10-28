use std::fs;
use std::path::PathBuf;
use std::process::Command;
use std::time::{SystemTime, UNIX_EPOCH};

fn binary() -> Command {
    Command::new(env!("CARGO_BIN_EXE_inventory-ledger"))
}

fn temporary_path(test_name: &str) -> PathBuf {
    let nonce = SystemTime::now().duration_since(UNIX_EPOCH).expect("clock after epoch").as_nanos();
    std::env::temp_dir().join(format!(
        "inventory-ledger-{test_name}-{}-{nonce}.db",
        std::process::id()
    ))
}

fn run(path: &PathBuf, args: &[&str]) -> std::process::Output {
    binary().env("INVENTORY_LEDGER_FILE", path).args(args).output().expect("run binary")
}

#[test]
fn separate_processes_share_persistent_state() {
    let path = temporary_path("persistent");
    let add = run(&path, &["add", "dial", "caliper"]);
    assert!(add.status.success());
    assert_eq!(String::from_utf8(add.stdout).expect("UTF-8"), "added 1: dial caliper\n");
    let checkout = run(&path, &["checkout", "1", "Grace", "Hopper"]);
    assert!(checkout.status.success());
    let list = run(&path, &["list"]);
    assert_eq!(
        String::from_utf8(list.stdout).expect("UTF-8"),
        "1 [checked-out: Grace Hopper] dial caliper\n"
    );
    fs::remove_file(path).expect("cleanup");
}

#[test]
fn failed_domain_operation_leaves_snapshot_unchanged() {
    let path = temporary_path("failure");
    assert!(run(&path, &["add", "gauge"]).status.success());
    let before = fs::read(&path).expect("snapshot");
    let failure = run(&path, &["return", "1"]);
    assert_eq!(failure.status.code(), Some(1));
    assert!(failure.stdout.is_empty());
    assert!(String::from_utf8(failure.stderr).expect("UTF-8").contains("cannot return item 1"));
    assert_eq!(fs::read(&path).expect("snapshot"), before);
    fs::remove_file(path).expect("cleanup");
}

#[test]
fn help_does_not_create_storage() {
    let path = temporary_path("help");
    let output = run(&path, &["help"]);
    assert!(output.status.success());
    assert!(!path.exists());
}
