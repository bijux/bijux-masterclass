use metricrail::app::{AppError, analyze_file, analyze_text};
use metricrail::config::Config;
use std::fs;
use std::sync::atomic::{AtomicU64, Ordering};

static NEXT_TEMPORARY: AtomicU64 = AtomicU64::new(0);

fn temporary_path() -> std::path::PathBuf {
    let sequence = NEXT_TEMPORARY.fetch_add(1, Ordering::Relaxed);
    std::env::temp_dir().join(format!(
        "metricrail-offline-{}-{sequence}.tsv",
        std::process::id()
    ))
}

#[test]
fn offline_analysis_reports_physical_line() {
    let input = "a\tx\t1\t1\n\ninvalid\n";
    match analyze_text(input, &Config::default()) {
        Err(AppError::Parse { line, .. }) => assert_eq!(line, 3),
        other => panic!("unexpected result: {other:?}"),
    }
}

#[test]
fn offline_analysis_enforces_record_limit() {
    let mut config = Config::default();
    config.max_offline_records = 1;
    let input = "a\tx\t1\t1\nb\ty\t1\t1\n";
    assert!(matches!(
        analyze_text(input, &config),
        Err(AppError::Usage(_))
    ));
}

#[test]
fn file_analysis_reads_at_most_the_configured_limit_plus_one() {
    let path = temporary_path();
    fs::write(&path, "a\tx\t1\t1\n").expect("fixture");
    let mut config = Config::default();
    config.max_offline_bytes = 5;
    config.max_line_bytes = 5;
    config.max_identifier_bytes = 5;
    let result = analyze_file(&path, &config);
    let _ = fs::remove_file(&path);
    assert!(matches!(result, Err(AppError::Usage(_))));
}
