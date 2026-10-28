
use framevault::process_capture::decode_capture;
use framevault::store::load;
use framevault::Limits;
use std::path::PathBuf;
use std::process::Command;
use std::time::{SystemTime, UNIX_EPOCH};

fn archive_path() -> PathBuf {
    let stamp = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .expect("clock after epoch")
        .as_nanos();
    std::env::temp_dir()
        .join(format!("framevault-capture-{}-{stamp}", std::process::id()))
        .join("capture.fv")
}

#[test]
fn capture_uses_direct_process_arguments_and_keeps_streams_separate() {
    let binary = env!("CARGO_BIN_EXE_framevault");
    let archive = archive_path();
    let output = Command::new(binary)
        .arg("capture")
        .arg(&archive)
        .arg("--")
        .arg(binary)
        .arg("__emit-test")
        .arg("stdout-value")
        .arg("stderr-value")
        .arg("7")
        .output()
        .expect("run framevault capture");
    assert!(output.status.success(), "{}", String::from_utf8_lossy(&output.stderr));

    let stored = load(&archive, Limits::default()).expect("load captured archive");
    let capture = decode_capture(stored.entries()[0].payload()).expect("decode capture");
    assert_eq!(capture.exit_code, Some(7));
    assert_eq!(capture.stdout, b"stdout-value");
    assert_eq!(capture.stderr, b"stderr-value");
    std::fs::remove_dir_all(archive.parent().expect("fixture parent")).expect("remove fixture");
}
