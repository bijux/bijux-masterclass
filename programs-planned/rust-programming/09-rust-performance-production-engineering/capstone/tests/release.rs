use metricrail::release::BuildInfo;

#[test]
fn version_output_is_stable_and_contains_artifact_identity() {
    let output = BuildInfo {
        package_version: "1.2.3",
        source_revision: "abc123",
        target: "x86_64-unknown-linux-gnu",
        profile: "dist",
        toolchain: "1.97.1",
    }
    .render();
    assert!(output.contains("package_version=1.2.3\n"));
    assert!(output.contains("source_revision=abc123\n"));
    assert!(!output.contains("timestamp"));
    assert!(!output.contains("/tmp/"));
}
