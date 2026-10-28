use std::{
    fs,
    path::PathBuf,
    time::{SystemTime, UNIX_EPOCH},
};

use axiomstore::{LendingRecords, Store};

#[cfg(unix)]
use axiomstore::Record;

fn temp_path(label: &str) -> PathBuf {
    let unique = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .expect("clock after epoch")
        .as_nanos();
    std::env::temp_dir().join(format!(
        "axiomstore-format-{label}-{}-{unique}.ax",
        std::process::id()
    ))
}

fn write_fixture(label: &str, bytes: &[u8]) -> PathBuf {
    let path = temp_path(label);
    fs::write(&path, bytes).expect("write fixture copy");
    path
}

fn checksum(bytes: &[u8]) -> u32 {
    bytes.iter().fold(2_166_136_261_u32, |hash, byte| {
        (hash ^ u32::from(*byte)).wrapping_mul(16_777_619)
    })
}

fn with_checksum(mut bytes: Vec<u8>) -> Vec<u8> {
    bytes.extend_from_slice(&checksum(&bytes).to_be_bytes());
    bytes
}

fn archive_prefix(count: u32) -> Vec<u8> {
    let mut bytes = b"AXIOM01\0".to_vec();
    bytes.extend_from_slice(&count.to_be_bytes());
    bytes
}

#[test]
fn immutable_empty_fixture_remains_readable() {
    let path = write_fixture("empty", include_bytes!("../fixtures/axiom01-empty.bin"));
    let store = Store::<256, 8>::new(&path).expect("store");
    assert!(store.open_snapshot().expect("fixture is valid").is_empty());
    fs::remove_file(path).expect("remove fixture copy");
}

#[test]
fn immutable_record_fixture_lends_canonical_rows() {
    let path = write_fixture(
        "two-records",
        include_bytes!("../fixtures/axiom01-two-records.bin"),
    );
    let store = Store::<256, 8>::new(&path).expect("store");
    let snapshot = store.open_snapshot().expect("fixture is valid");
    let mut cursor = snapshot.records();
    assert_eq!(
        cursor.next().expect("first").expect("valid").key(),
        "alpha"
    );
    assert_eq!(
        cursor.next().expect("second").expect("valid").key(),
        "beta"
    );
    assert!(cursor.next().is_none());
    fs::remove_file(path).expect("remove fixture copy");
}

#[test]
fn lent_fields_point_into_the_verified_snapshot_bytes() {
    let path = write_fixture(
        "borrowed-view",
        include_bytes!("../fixtures/axiom01-two-records.bin"),
    );
    let store = Store::<256, 8>::new(&path).expect("store");
    let snapshot = store.open_snapshot().expect("fixture is valid");
    let start = snapshot.bytes().as_ptr() as usize;
    let end = start + snapshot.bytes().len();
    let mut cursor = snapshot.records();
    let view = cursor.next().expect("first").expect("valid");
    let key_start = view.key().as_ptr() as usize;
    let key_end = key_start + view.key().len();
    let value_start = view.value().as_ptr() as usize;
    let value_end = value_start + view.value().len();

    assert!((start..=end).contains(&key_start));
    assert!(key_end <= end);
    assert!((start..=end).contains(&value_start));
    assert!(value_end <= end);
    fs::remove_file(path).expect("remove fixture copy");
}

#[test]
fn valid_checksum_does_not_make_noncanonical_order_valid() {
    let path = write_fixture(
        "noncanonical",
        include_bytes!("../fixtures/axiom01-noncanonical.bin"),
    );
    let store = Store::<256, 8>::new(&path).expect("store");
    let error = store.open_snapshot().expect_err("order must be rejected");
    assert!(error.to_string().contains("strictly ordered"));
    fs::remove_file(path).expect("remove fixture copy");
}

#[test]
fn valid_checksum_does_not_make_duplicate_keys_valid() {
    let path = write_fixture(
        "duplicate",
        include_bytes!("../fixtures/axiom01-duplicate.bin"),
    );
    let store = Store::<256, 8>::new(&path).expect("store");
    let error = store.open_snapshot().expect_err("duplicate must be rejected");
    assert!(error.to_string().contains("strictly ordered"));
    fs::remove_file(path).expect("remove fixture copy");
}

#[test]
fn corruption_is_reported_as_checksum_failure() {
    let mut bytes = include_bytes!("../fixtures/axiom01-two-records.bin").to_vec();
    let last = bytes.len() - 1;
    bytes[last] ^= 0x55;
    let path = write_fixture("corrupt", &bytes);
    let store = Store::<256, 8>::new(&path).expect("store");
    let error = store.open_snapshot().expect_err("checksum must fail");
    assert!(error.to_string().contains("checksum"));
    fs::remove_file(path).expect("remove fixture copy");
}

#[test]
fn hostile_key_length_is_rejected_before_payload_access() {
    let mut bytes = archive_prefix(1);
    bytes.extend_from_slice(&u32::MAX.to_be_bytes());
    let path = write_fixture("hostile-length", &with_checksum(bytes));
    let store = Store::<64, 8>::new(&path).expect("store");
    let error = store.open_snapshot().expect_err("limit must be enforced");
    assert!(error.to_string().contains("declared key"));
    fs::remove_file(path).expect("remove fixture copy");
}

#[test]
fn valid_checksum_does_not_hide_trailing_bytes() {
    let mut bytes = archive_prefix(0);
    bytes.push(0xaa);
    let path = write_fixture("trailing", &with_checksum(bytes));
    let store = Store::<64, 8>::new(&path).expect("store");
    let error = store.open_snapshot().expect_err("trailing byte must fail");
    assert!(error.to_string().contains("trailing"));
    fs::remove_file(path).expect("remove fixture copy");
}

#[test]
fn invalid_utf8_reports_the_field_boundary() {
    let mut bytes = archive_prefix(1);
    bytes.extend_from_slice(&1_u32.to_be_bytes());
    bytes.push(0xff);
    bytes.extend_from_slice(&0_u32.to_be_bytes());
    let path = write_fixture("utf8", &with_checksum(bytes));
    let store = Store::<64, 8>::new(&path).expect("store");
    let error = store.open_snapshot().expect_err("UTF-8 must fail");
    assert!(error.to_string().contains("UTF-8"));
    fs::remove_file(path).expect("remove fixture copy");
}

#[test]
fn impossible_record_count_is_rejected_without_iteration() {
    let path = write_fixture("count", &with_checksum(archive_prefix(2)));
    let store = Store::<64, 8>::new(&path).expect("store");
    let error = store.open_snapshot().expect_err("count cannot fit");
    assert!(error.to_string().contains("cannot fit"));
    fs::remove_file(path).expect("remove fixture copy");
}

#[test]
fn truncated_archive_is_rejected_without_panicking() {
    let path = write_fixture("truncated", b"AXIOM01");
    let store = Store::<64, 8>::new(&path).expect("store");
    let error = store.open_snapshot().expect_err("truncation must fail");
    assert!(error.to_string().contains("header") || error.to_string().contains("checksum"));
    fs::remove_file(path).expect("remove fixture copy");
}

#[cfg(unix)]
#[test]
fn writer_matches_the_checked_in_canonical_fixture() {
    let path = temp_path("writer");
    let store = Store::<256, 8>::new(&path).expect("store");
    store.init().expect("initialize");
    store
        .put(Record::new("beta", "two").expect("record"))
        .expect("put beta");
    let snapshot = store
        .put(Record::new("alpha", "one").expect("record"))
        .expect("put alpha");
    assert_eq!(
        snapshot.bytes(),
        include_bytes!("../fixtures/axiom01-two-records.bin")
    );
    fs::remove_file(path).expect("remove archive");
}
