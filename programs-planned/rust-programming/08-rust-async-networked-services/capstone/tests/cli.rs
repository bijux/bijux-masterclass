use std::process::Command;

#[test]
fn demo_runs_a_complete_service_scenario() {
    let output = Command::new(env!("CARGO_BIN_EXE_jobwire"))
        .arg("demo")
        .output()
        .expect("run jobwire demo");
    assert!(output.status.success(), "stderr: {}", String::from_utf8_lossy(&output.stderr));
    let stdout = String::from_utf8(output.stdout).unwrap();
    assert!(stdout.contains("result=HELLO ASYNC RUST"));
    assert!(stdout.contains("completed_jobs=1"));
}
