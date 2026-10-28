use memory_workspace::{
    Workspace, WorkspaceError
};
use std::panic::{
    catch_unwind, AssertUnwindSafe
};
#[test]
fn staged_edits_do_not_touch_live_state_before_commit() {
    let mut workspace = Workspace::new();
    let handle = workspace.add("title", "original").unwrap_or_else(|error| panic!("{error}"));
    let mut session = workspace.begin_edit(handle).unwrap_or_else(|error| panic!("{error}"));
    session.set_text("working");
    assert_eq!(workspace.view(handle).map(|view| view.text().to_owned()), Ok(String::from("original")));
    let receipt = workspace.commit(session).unwrap_or_else(|failure| panic!("{}", failure.error));
    assert_eq!(receipt.revision, 1);
    assert_eq!(workspace.view(handle).map(|view| view.text().to_owned()), Ok(String::from("working")));
}
#[test]
fn conflict_returns_the_owned_session() {
    let mut workspace = Workspace::new();
    let handle = workspace.add("title", "zero").unwrap_or_else(|error| panic!("{error}"));
    let mut old = workspace.begin_edit(handle).unwrap_or_else(|error| panic!("{error}"));
    let mut current = workspace.begin_edit(handle).unwrap_or_else(|error| panic!("{error}"));
    current.set_text("one");
    assert!(workspace.commit(current).is_ok());
    old.set_text("stale");
    let failure = match workspace.commit(old) {
        Ok(_) => panic!("expected conflict"), Err(value) => value
    };
    assert!(matches!(failure.error, WorkspaceError::RevisionConflict {
        expected: 0, actual: 1, ..
    }));
    assert_eq!(failure.session.text(), "stale");
    assert_eq!(workspace.view(handle).map(|view| view.text().to_owned()), Ok(String::from("one")));
}
#[test]
fn panic_while_editing_discards_only_working_state() {
    let mut workspace = Workspace::new();
    let handle = workspace.add("title", "live").unwrap_or_else(|error| panic!("{error}"));
    let result = catch_unwind(AssertUnwindSafe(|| {
        let mut session = workspace.begin_edit(handle).unwrap_or_else(|error| panic!("{error}"));
        session.set_text("temporary");
        panic!("intentional");
    }));
    assert!(result.is_err());
    assert_eq!(workspace.view(handle).map(|view| view.text().to_owned()), Ok(String::from("live")));
}
