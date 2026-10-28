use memory_workspace::ScriptEngine;
use std::fs;
use std::process::Command;
use std::time::{SystemTime, UNIX_EPOCH};

#[test]
fn script_engine_exercises_snapshot_liveness() {
    let script = concat!(
        "ADD\tdoc\tTitle\told\n",
        "SNAPSHOT\tsnap\tdoc\n",
        "WATCH\twatch\tsnap\n",
        "EDIT\tdoc\t0\tnew\n",
        "EVICT\tdoc\t0\n",
        "DROP-SNAPSHOT\tsnap\n",
        "CHECK-WATCH\twatch\n",
    );
    let output = ScriptEngine::new()
        .execute(script)
        .unwrap_or_else(|error| panic!("{error}"));
    assert_eq!(
        output.last().map(String::as_str),
        Some("WATCH\twatch\texpired")
    );
}

#[test]
fn real_demo_binary_succeeds() {
    let output = Command::new(env!("CARGO_BIN_EXE_memory-workspace"))
        .arg("demo")
        .output()
        .unwrap_or_else(|error| panic!("{error}"));
    assert!(output.status.success());
    let stdout = String::from_utf8(output.stdout)
        .unwrap_or_else(|error| panic!("{error}"));
    assert!(stdout.contains("WATCH\twatch0\texpired"));
    assert!(stdout.contains("MEMORY\t"));
}

#[test]
fn real_script_file_is_executed() {
    let nonce = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap_or_default()
        .as_nanos();
    let path = std::env::temp_dir().join(format!(
        "memory-workspace-{}-{nonce}.script",
        std::process::id()
    ));
    fs::write(&path, "ADD\tdoc\tTitle\tText\nSHOW\tdoc\n")
        .unwrap_or_else(|error| panic!("{error}"));
    let output = Command::new(env!("CARGO_BIN_EXE_memory-workspace"))
        .arg("script")
        .arg(&path)
        .output()
        .unwrap_or_else(|error| panic!("{error}"));
    let _ = fs::remove_file(&path);
    assert!(output.status.success());
    assert!(String::from_utf8_lossy(&output.stdout).contains("DOCUMENT"));
}
