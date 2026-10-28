use std::{
    fs,
    path::PathBuf,
    time::{SystemTime, UNIX_EPOCH},
};

use axiomstore::{migrate_v0, LendingRecords, Store};

fn temp_path(suffix: &str) -> PathBuf {
    let unique = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .expect("clock after epoch")
        .as_nanos();
    std::env::temp_dir().join(format!(
        "axiomstore-migrate-{suffix}-{}-{unique}",
        std::process::id()
    ))
}

#[test]
fn legacy_values_may_contain_additional_delimiters() {
    let source = temp_path("source.txt");
    let destination = temp_path("destination.ax");
    fs::write(&source, "alpha=one\nbeta=two=with=equals\n").expect("write source");
    let store = Store::<256, 4>::new(&destination).expect("store");
    let snapshot = migrate_v0(&source, &store).expect("migrate");
    let mut cursor = snapshot.records();
    assert_eq!(
        cursor.next().expect("first").expect("valid").key(),
        "alpha"
    );
    assert_eq!(
        cursor.next().expect("second").expect("valid").value(),
        "two=with=equals"
    );
    fs::remove_file(source).expect("remove source");
    fs::remove_file(destination).expect("remove destination");
}

#[test]
fn malformed_legacy_input_preserves_source_and_does_not_create_destination() {
    let source = temp_path("bad.txt");
    let destination = temp_path("bad.ax");
    let original = "valid=one\ninvalid\n";
    fs::write(&source, original).expect("write source");
    let store = Store::<256, 4>::new(&destination).expect("store");
    let error = migrate_v0(&source, &store).expect_err("line two should fail");
    assert!(error.to_string().contains("line 2"));
    assert_eq!(fs::read_to_string(&source).expect("source remains"), original);
    assert!(!destination.exists());
    fs::remove_file(source).expect("remove source");
}

#[test]
fn migration_refuses_to_replace_an_existing_destination() {
    let source = temp_path("existing-source.txt");
    let destination = temp_path("existing.ax");
    fs::write(&source, "alpha=one\n").expect("write source");
    fs::write(&destination, b"existing bytes").expect("write destination");
    let store = Store::<256, 4>::new(&destination).expect("store");
    let error = migrate_v0(&source, &store).expect_err("destination exists");
    assert!(error.to_string().contains("already exists"));
    assert_eq!(
        fs::read(&destination).expect("destination remains"),
        b"existing bytes"
    );
    fs::remove_file(source).expect("remove source");
    fs::remove_file(destination).expect("remove destination");
}
