#![cfg(unix)]

use std::{
    fs,
    path::PathBuf,
    process::Command,
    time::{SystemTime, UNIX_EPOCH},
};

fn temp_path() -> PathBuf {
    let unique = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .expect("clock after epoch")
        .as_nanos();
    std::env::temp_dir().join(format!(
        "axiomstore-cli-{}-{unique}.ax",
        std::process::id()
    ))
}

#[test]
fn real_binary_preserves_command_and_exit_contracts() {
    let binary = env!("CARGO_BIN_EXE_axiomstore");
    let path = temp_path();

    let init = Command::new(binary)
        .arg("init")
        .arg(&path)
        .output()
        .expect("run init");
    assert!(init.status.success());

    let put = Command::new(binary)
        .arg("put")
        .arg(&path)
        .args(["a", "one"])
        .output()
        .expect("run put");
    assert!(put.status.success());

    let list = Command::new(binary)
        .arg("list")
        .arg(&path)
        .output()
        .expect("run list");
    assert!(list.status.success());
    assert_eq!(String::from_utf8(list.stdout).expect("UTF-8"), "a\tone\n");

    let usage = Command::new(binary)
        .arg("put")
        .arg(&path)
        .output()
        .expect("run invalid command");
    assert_eq!(usage.status.code(), Some(2));
    assert!(String::from_utf8(usage.stderr)
        .expect("UTF-8")
        .contains("usage"));

    fs::remove_file(path).expect("remove archive");
}
