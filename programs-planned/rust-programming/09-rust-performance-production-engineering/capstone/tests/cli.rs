use std::fs;
use std::process::Command;
use std::sync::atomic::{AtomicU64, Ordering};
use std::time::{SystemTime, UNIX_EPOCH};

static NEXT_TEMPORARY: AtomicU64 = AtomicU64::new(0);

fn temporary_path() -> std::path::PathBuf {
    let time = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .expect("system time")
        .as_nanos();
    let sequence = NEXT_TEMPORARY.fetch_add(1, Ordering::Relaxed);
    std::env::temp_dir().join(format!(
        "metricrail-{}-{time}-{sequence}.tsv",
        std::process::id()
    ))
}

#[test]
fn analyze_command_renders_sorted_output() {
    let path = temporary_path();
    fs::write(&path, "z\tb\t1\t1\na\tb\t1\t2\n").expect("fixture");
    let output = Command::new(env!("CARGO_BIN_EXE_metricrail"))
        .args(["analyze", path.to_str().expect("UTF-8 path")])
        .output()
        .expect("run");
    let _ = fs::remove_file(&path);
    assert!(output.status.success());
    let stdout = String::from_utf8(output.stdout).expect("UTF-8 output");
    assert!(stdout.starts_with("a\tb\t1\t2"));
}

#[test]
fn version_has_no_wall_clock_field() {
    let output = Command::new(env!("CARGO_BIN_EXE_metricrail"))
        .arg("version")
        .output()
        .expect("run");
    assert!(output.status.success());
    let stdout = String::from_utf8(output.stdout).expect("UTF-8 output");
    assert!(stdout.contains("package_version="));
    assert!(stdout.contains("target="));
    assert!(!stdout.contains("timestamp"));
}
