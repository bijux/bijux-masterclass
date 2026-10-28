use metricrail::config::Config;
use metricrail::parse::parse_record;
use metricrail::store::Store;

#[test]
fn accepted_records_produce_a_deterministic_snapshot() {
    let config = Config::default();
    let mut store = Store::new(config.max_series, config.max_identifier_storage_bytes);
    for line in [
        "z\tb\t1\t1",
        "a\tc\t1\t2",
        "a\tb\t1\t3",
        "a\tb\t2\t4",
    ] {
        let record = parse_record(line, config.max_line_bytes, config.max_identifier_bytes)
            .expect("valid record");
        store.apply(record).expect("apply");
    }
    let rendered = store
        .snapshot()
        .render(config.max_snapshot_bytes)
        .expect("render");
    let lines: Vec<_> = rendered.lines().collect();
    assert_eq!(lines.len(), 3);
    assert!(lines[0].starts_with("a\tb\t2\t7"));
    assert!(lines[1].starts_with("a\tc\t1\t2"));
    assert!(lines[2].starts_with("z\tb\t1\t1"));
}

#[test]
fn old_timestamp_does_not_partially_mutate_series() {
    let config = Config::default();
    let mut store = Store::new(config.max_series, config.max_identifier_storage_bytes);
    let first = parse_record("a\tb\t10\t2", 128, 32).expect("first");
    let old = parse_record("a\tb\t9\t100", 128, 32).expect("old");
    store.apply(first).expect("first apply");
    let before = store.snapshot();
    assert!(store.apply(old).is_err());
    assert_eq!(store.snapshot(), before);
}
