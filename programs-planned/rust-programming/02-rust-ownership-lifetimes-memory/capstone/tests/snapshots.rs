use memory_workspace::{SnapshotKey, SnapshotWatcher, Workspace};
use std::rc::Rc;

#[test]
fn repeated_snapshot_requests_share_one_retained_allocation() {
    let mut workspace = Workspace::new();
    let handle = workspace
        .add("title", "text")
        .unwrap_or_else(|error| panic!("{error}"));
    let first = workspace
        .snapshot(handle)
        .unwrap_or_else(|error| panic!("{error}"));
    let second = workspace
        .snapshot(handle)
        .unwrap_or_else(|error| panic!("{error}"));
    assert!(Rc::ptr_eq(&first, &second));
}

#[test]
fn weak_watcher_does_not_preserve_evicted_snapshot() {
    let mut workspace = Workspace::new();
    let handle = workspace
        .add("title", "text")
        .unwrap_or_else(|error| panic!("{error}"));
    let snapshot = workspace
        .snapshot(handle)
        .unwrap_or_else(|error| panic!("{error}"));
    let key = snapshot.key();
    let watcher = SnapshotWatcher::new(&snapshot);
    assert!(workspace.evict_snapshot(key));
    drop(snapshot);
    assert!(watcher.upgrade().is_none());
}

#[test]
fn old_revision_snapshot_remains_immutable_after_edit() {
    let mut workspace = Workspace::new();
    let handle = workspace
        .add("title", "old")
        .unwrap_or_else(|error| panic!("{error}"));
    let old = workspace
        .snapshot(handle)
        .unwrap_or_else(|error| panic!("{error}"));
    let mut session = workspace
        .begin_edit(handle)
        .unwrap_or_else(|error| panic!("{error}"));
    session.set_text("new");
    assert!(workspace.commit(session).is_ok());
    let new = workspace
        .snapshot(handle)
        .unwrap_or_else(|error| panic!("{error}"));
    assert_eq!(old.text(), "old");
    assert_eq!(new.text(), "new");
    assert_eq!(old.key(), SnapshotKey { handle, revision: 0 });
    assert_eq!(new.key(), SnapshotKey { handle, revision: 1 });
}

#[test]
fn snapshot_retention_is_bounded_and_fifo() {
    let mut workspace = Workspace::with_snapshot_limit(2);
    let first_handle = workspace
        .add("one", "first")
        .unwrap_or_else(|error| panic!("{error}"));
    let second_handle = workspace
        .add("two", "second")
        .unwrap_or_else(|error| panic!("{error}"));
    let third_handle = workspace
        .add("three", "third")
        .unwrap_or_else(|error| panic!("{error}"));

    let first = workspace
        .snapshot(first_handle)
        .unwrap_or_else(|error| panic!("{error}"));
    let first_watcher = SnapshotWatcher::new(&first);
    drop(first);
    let _second = workspace
        .snapshot(second_handle)
        .unwrap_or_else(|error| panic!("{error}"));
    let _third = workspace
        .snapshot(third_handle)
        .unwrap_or_else(|error| panic!("{error}"));

    assert_eq!(workspace.retained_snapshot_count(), 2);
    assert!(first_watcher.upgrade().is_none());
}

#[test]
fn zero_limit_disables_workspace_retention() {
    let mut workspace = Workspace::with_snapshot_limit(0);
    let handle = workspace
        .add("title", "text")
        .unwrap_or_else(|error| panic!("{error}"));
    let first = workspace
        .snapshot(handle)
        .unwrap_or_else(|error| panic!("{error}"));
    let second = workspace
        .snapshot(handle)
        .unwrap_or_else(|error| panic!("{error}"));
    assert!(!Rc::ptr_eq(&first, &second));
    assert_eq!(workspace.retained_snapshot_count(), 0);
}
