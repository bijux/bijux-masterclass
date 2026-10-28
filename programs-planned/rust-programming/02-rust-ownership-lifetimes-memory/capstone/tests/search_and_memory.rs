use memory_workspace::{with_normalized_query, Workspace};

#[test]
fn search_returns_borrowed_matches_and_durable_ranges() {
    let mut workspace = Workspace::new();
    let handle = workspace
        .add("notes", "memory first\nmemory second")
        .unwrap_or_else(|error| panic!("{error}"));
    let matches = workspace.search(" memory ");
    assert_eq!(matches.len(), 2);
    assert_eq!(matches[0].handle, handle);
    assert_eq!(matches[0].matched, "memory");
    assert_eq!(matches[0].line, Some(0));
    assert_eq!(
        &workspace
            .view(handle)
            .unwrap_or_else(|error| panic!("{error}"))
            .text()[matches[1].range.clone()],
        "memory"
    );
}

#[test]
fn search_normalizes_only_the_query() {
    let mut workspace = Workspace::new();
    workspace
        .add("notes", "one  two\none two")
        .unwrap_or_else(|error| panic!("{error}"));
    let matches = workspace.search(" one\t two ");
    assert_eq!(matches.len(), 1);
    assert_eq!(matches[0].matched, "one two");
}

#[test]
fn memory_report_deduplicates_shared_snapshot_cache() {
    let mut workspace = Workspace::new();
    let handle = workspace
        .add("title", "payload")
        .unwrap_or_else(|error| panic!("{error}"));
    let first = workspace
        .snapshot(handle)
        .unwrap_or_else(|error| panic!("{error}"));
    let second = workspace
        .snapshot(handle)
        .unwrap_or_else(|error| panic!("{error}"));
    let report = workspace.memory_report();
    assert_eq!(report.snapshot_cache_entries, 1);
    assert_eq!(report.unique_snapshot_allocations, 1);
    assert_eq!(first.payload_bytes(), second.payload_bytes());
    assert!(!report.exclusions.is_empty());
    assert_eq!(
        report.live_payload_bytes(),
        report.title_payload_bytes + report.text_payload_bytes + report.tag_payload_bytes
    );
}

#[test]
fn scoped_query_can_export_owned_but_not_borrowed_temporary_data() {
    let borrowed_path = with_normalized_query(" query ", str::to_owned);
    let owned_path = with_normalized_query("query\twith   gaps", str::to_owned);
    assert_eq!(borrowed_path, "query");
    assert_eq!(owned_path, "query with gaps");
}
