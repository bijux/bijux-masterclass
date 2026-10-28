use std::io::Cursor;
use taskboard::{
    Command, Priority, Status, Task, TaskBoard, TaskError, TaskId, execute, load_from, save_to,
};

fn id(value: u64) -> TaskId {
    TaskId::new(value).expect("test ID is nonzero")
}

#[test]
fn public_consumer_can_complete_a_full_lifecycle_without_field_access() {
    let mut board = TaskBoard::new();
    let task_id = board
        .add(Priority::High, String::from("Stabilize storage"))
        .expect("valid task");

    board.start(task_id).expect("todo may start");
    board.complete(task_id).expect("doing may complete");
    assert_eq!(board.find(task_id).map(Task::status), Some(Status::Done));

    board.reopen(task_id).expect("done may reopen");
    assert_eq!(board.find(task_id).map(Task::status), Some(Status::Todo));
}

#[test]
fn public_consumer_observes_domain_failure_without_partial_transition() {
    let mut board = TaskBoard::new();
    let task_id = board
        .add(Priority::Normal, String::from("Write tests"))
        .expect("valid task");

    assert!(matches!(
        board.complete(task_id),
        Err(TaskError::IllegalTransition {
            from: Status::Todo,
            ..
        })
    ));
    assert_eq!(board.find(task_id).map(Task::status), Some(Status::Todo));
}

#[test]
fn public_consumer_can_rename_without_accessing_private_fields() {
    let mut board = TaskBoard::new();
    let task_id = board
        .add(Priority::Normal, String::from("First title"))
        .expect("valid task");

    board
        .rename(task_id, String::from("Second title"))
        .expect("valid title");
    assert_eq!(board.find(task_id).map(Task::title), Some("Second title"));

    assert_eq!(
        board.rename(task_id, String::from("\n")),
        Err(TaskError::EmptyTitle)
    );
    assert_eq!(board.find(task_id).map(Task::title), Some("Second title"));
}

#[test]
fn public_codec_round_trip_preserves_all_exposed_values() {
    let mut board = TaskBoard::new();
    let first = board
        .add(Priority::High, String::from("Repair parser"))
        .expect("valid task");
    let second = board
        .add(Priority::Low, String::from("Polish docs"))
        .expect("valid task");
    board.start(first).expect("todo may start");
    board.start(second).expect("todo may start");
    board.complete(second).expect("doing may complete");

    let mut bytes = Vec::new();
    save_to(&mut bytes, &board).expect("memory writer");
    let restored = load_from(Cursor::new(bytes)).expect("valid stored board");

    let exposed: Vec<_> = restored
        .tasks()
        .iter()
        .map(|task| (task.id(), task.title(), task.priority(), task.status()))
        .collect();
    assert_eq!(
        exposed,
        vec![
            (id(1), "Repair parser", Priority::High, Status::Doing),
            (id(2), "Polish docs", Priority::Low, Status::Done),
        ]
    );
}

#[test]
fn typed_execution_separates_state_change_from_rendering() {
    let mut board = TaskBoard::new();
    let outcome = execute(
        &mut board,
        Command::Add {
            priority: Priority::Normal,
            title: String::from("Review ownership ledger"),
        },
    )
    .expect("valid add");
    assert!(outcome.changed_state());
    assert_eq!(outcome.output(), "added task 1\n");

    let list = execute(&mut board, Command::List { status: None }).expect("valid list");
    assert!(!list.changed_state());
    assert!(list.output().contains("Review ownership ledger"));
}
