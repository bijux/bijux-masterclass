use std::error::Error;
use std::fs;
use std::io::{self, Cursor, Write};
use std::path::PathBuf;
use std::sync::atomic::{AtomicU64, Ordering};
use std::time::{SystemTime, UNIX_EPOCH};
use taskboard::{
    Priority, RecordError, Status, StorageError, Task, TaskBoard, TaskError, load_from, load_path,
    save_path, save_to,
};

static COUNTER: AtomicU64 = AtomicU64::new(0);

struct Sandbox {
    root: PathBuf,
}

impl Sandbox {
    fn new() -> Self {
        let nonce = COUNTER.fetch_add(1, Ordering::Relaxed);
        let nanos = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .map_or(0_u128, |duration| duration.as_nanos());
        let root = std::env::temp_dir().join(format!(
            "taskboard-persistence-test-{}-{nanos}-{nonce}",
            std::process::id()
        ));
        fs::create_dir(&root).expect("unique sandbox directory");
        Self { root }
    }

    fn path(&self, name: &str) -> PathBuf {
        self.root.join(name)
    }

    fn temporary_entries_for(&self, target_name: &str) -> Vec<PathBuf> {
        let prefix = format!(".{target_name}.tmp.");
        fs::read_dir(&self.root)
            .expect("sandbox is readable")
            .filter_map(Result::ok)
            .map(|entry| entry.path())
            .filter(|path| {
                path.file_name()
                    .and_then(|name| name.to_str())
                    .is_some_and(|name| name.starts_with(&prefix))
            })
            .collect()
    }
}

impl Drop for Sandbox {
    fn drop(&mut self) {
        let _ignored = fs::remove_dir_all(&self.root);
    }
}

struct FailingWriter {
    remaining: usize,
    accepted: Vec<u8>,
}

impl FailingWriter {
    fn new(remaining: usize) -> Self {
        Self {
            remaining,
            accepted: Vec::new(),
        }
    }
}

impl Write for FailingWriter {
    fn write(&mut self, buffer: &[u8]) -> io::Result<usize> {
        if self.remaining == 0 {
            return Err(io::Error::new(
                io::ErrorKind::WriteZero,
                "injected writer exhaustion",
            ));
        }
        let accepted = buffer.len().min(self.remaining);
        self.accepted.extend_from_slice(&buffer[..accepted]);
        self.remaining -= accepted;
        Ok(accepted)
    }

    fn flush(&mut self) -> io::Result<()> {
        Ok(())
    }
}

fn sample_board() -> TaskBoard {
    let mut board = TaskBoard::new();
    let first = board
        .add(Priority::High, String::from("Repair parser"))
        .expect("valid task");
    let second = board
        .add(Priority::Normal, String::from("Write tests"))
        .expect("valid task");
    board.start(first).expect("todo may start");
    board
        .rename(second, String::from("Write persistence tests"))
        .expect("valid rename");
    board
}

#[test]
fn missing_path_has_a_narrow_empty_board_meaning() {
    let sandbox = Sandbox::new();
    let path = sandbox.path("absent.taskboard");
    let board = load_path(&path).expect("missing path starts an empty board");
    assert!(board.tasks().is_empty());
    assert!(!path.exists());
}

#[test]
fn path_round_trip_is_canonical_and_preserves_public_values() {
    let sandbox = Sandbox::new();
    let path = sandbox.path("board.taskboard");
    let board = sample_board();

    save_path(&path, &board).expect("valid board saves");
    assert_eq!(
        fs::read_to_string(&path).expect("saved text is readable"),
        concat!(
            "TASKBOARD-V1\n",
            "NEXT_ID\t3\n",
            "TASK\t1\tdoing\thigh\tRepair parser\n",
            "TASK\t2\ttodo\tnormal\tWrite persistence tests\n",
        )
    );

    let restored = load_path(&path).expect("saved board loads");
    let observed: Vec<_> = restored
        .tasks()
        .iter()
        .map(|task| (task.id(), task.title(), task.priority(), task.status()))
        .collect();
    assert_eq!(observed.len(), 2);
    assert_eq!(observed[0].1, "Repair parser");
    assert_eq!(observed[0].3, Status::Doing);
    assert_eq!(observed[1].1, "Write persistence tests");
}

#[test]
fn checked_in_valid_fixture_round_trips_without_semantic_loss() {
    let fixture = include_str!("../fixtures/valid-v1.taskboard");
    let board = load_from(Cursor::new(fixture)).expect("fixture is valid");
    let before: Vec<_> = board
        .tasks()
        .iter()
        .map(|task| (task.id(), task.title(), task.priority(), task.status()))
        .collect();

    let mut encoded = Vec::new();
    save_to(&mut encoded, &board).expect("memory writer succeeds");
    let reloaded = load_from(Cursor::new(encoded)).expect("canonical output reloads");
    let after: Vec<_> = reloaded
        .tasks()
        .iter()
        .map(|task| (task.id(), task.title(), task.priority(), task.status()))
        .collect();
    assert_eq!(before, after);
}

#[test]
fn corruption_fixtures_fail_in_the_intended_layer() {
    let malformed = load_from(Cursor::new(include_str!(
        "../fixtures/malformed-record.taskboard"
    )))
    .expect_err("malformed status must fail");
    assert!(matches!(
        malformed,
        StorageError::InvalidRecord {
            line: 3,
            source: RecordError::InvalidStatus(_),
        }
    ));

    let duplicate = load_from(Cursor::new(include_str!(
        "../fixtures/duplicate-id.taskboard"
    )))
    .expect_err("duplicate ID must fail");
    assert!(matches!(
        duplicate,
        StorageError::InvalidSnapshot(TaskError::DuplicateId(_))
    ));

    let invalid_next = load_from(Cursor::new(include_str!(
        "../fixtures/invalid-next-id.taskboard"
    )))
    .expect_err("allocator metadata collision must fail");
    assert!(matches!(
        invalid_next,
        StorageError::InvalidSnapshot(TaskError::InvalidNextId)
    ));

    let blank = load_from(Cursor::new(include_str!(
        "../fixtures/blank-record.taskboard"
    )))
    .expect_err("blank records are not silently skipped");
    assert!(matches!(
        blank,
        StorageError::InvalidRecord {
            line: 3,
            source: RecordError::UnknownTag(_),
        }
    ));
}

#[test]
fn generic_writer_failure_preserves_context_and_source() {
    let board = sample_board();
    let mut writer = FailingWriter::new(18);
    let error = save_to(&mut writer, &board).expect_err("injected writer must fail");

    assert!(matches!(error, StorageError::Io { .. }));
    assert!(error.to_string().contains("write"));
    assert!(error
        .source()
        .is_some_and(|source| source.to_string().contains("injected writer exhaustion")));
    assert!(!writer.accepted.is_empty());
}

#[test]
fn failed_path_commit_removes_its_temporary_file() {
    let sandbox = Sandbox::new();
    let target = sandbox.path("occupied");
    fs::create_dir(&target).expect("target directory exists");

    let error = save_path(&target, &sample_board()).expect_err("rename over directory must fail");
    assert!(matches!(error, StorageError::Io { .. }));
    assert!(target.is_dir());
    assert!(sandbox.temporary_entries_for("occupied").is_empty());
}

#[test]
fn save_does_not_create_a_missing_parent_directory_implicitly() {
    let sandbox = Sandbox::new();
    let path = sandbox.path("missing-parent/board.taskboard");
    let error = save_path(&path, &sample_board()).expect_err("missing parent is an I/O failure");
    assert!(matches!(error, StorageError::Io { .. }));
    assert!(!path.exists());
}
