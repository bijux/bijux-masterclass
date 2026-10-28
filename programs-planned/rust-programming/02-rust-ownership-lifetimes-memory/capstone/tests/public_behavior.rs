use memory_workspace::{
    DocumentHandle, HandleBuildError, ParseHandleError, Workspace, WorkspaceError
};
#[test]
fn stale_handles_are_rejected_after_slot_reuse() {
    let mut workspace = Workspace::new();
    let first = workspace
    .add("first", "text")
    .unwrap_or_else(|error| panic!("{error}"));
    assert_eq!(
    workspace.remove(first).map(|removed| removed.title),
    Ok(String::from("first"))
    );
    let second = workspace
    .add("second", "text")
    .unwrap_or_else(|error| panic!("{error}"));
    assert_eq!(first.slot(), second.slot());
    assert_ne!(first.generation(), second.generation());
    assert!(matches!(
    workspace.view(first),
    Err(WorkspaceError::StaleHandle {
        ..
    })
    ));
}
#[test]
fn borrowed_views_and_lines_follow_workspace_lifetime() {
    let mut workspace = Workspace::new();
    let handle = workspace
    .add("title", "line one\nline two")
    .unwrap_or_else(|error| panic!("{error}"));
    let view = workspace
    .view(handle)
    .unwrap_or_else(|error| panic!("{error}"));
    assert_eq!(view.title(), "title");
    assert_eq!(workspace.line(handle, 1), Ok(Some("line two")));
    assert_eq!(
    workspace.cache_stats(handle).map(|stats| stats.misses),
    Ok(1)
    );
}
#[test]
fn handle_round_trip_preserves_the_nonzero_invariant() {
    let handle = DocumentHandle::try_from_parts(7, 9)
    .unwrap_or_else(|error| panic!("{error}"));
    let parsed: Result<DocumentHandle, _> = handle.to_string().parse();
    assert!(matches!(parsed, Ok(value) if value == handle));
    assert_eq!(
    DocumentHandle::try_from_parts(0, 0),
    Err(HandleBuildError::ZeroGeneration)
    );
    assert!(matches!(
    "0:0".parse::<DocumentHandle>(),
    Err(ParseHandleError::ZeroGeneration)
    ));
}
