use std::ffi::OsStr;
use std::fs;
use std::path::{Path, PathBuf};
use std::process::{Command, Output};
use std::sync::atomic::{AtomicU64, Ordering};
use std::time::{SystemTime, UNIX_EPOCH};

static COUNTER: AtomicU64 = AtomicU64::new(0);

struct Sandbox {
    root: PathBuf,
    storage: PathBuf,
}

impl Sandbox {
    fn new() -> Self {
        let nonce = COUNTER.fetch_add(1, Ordering::Relaxed);
        let nanos = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .map_or(0_u128, |duration| duration.as_nanos());
        let root = std::env::temp_dir().join(format!(
            "taskboard-cli-test-{}-{nanos}-{nonce}",
            std::process::id()
        ));
        fs::create_dir(&root).expect("unique sandbox directory");
        let storage = root.join("board.db");
        Self { root, storage }
    }

    fn run<I, S>(&self, arguments: I) -> Output
    where
        I: IntoIterator<Item = S>,
        S: AsRef<OsStr>,
    {
        Command::new(env!("CARGO_BIN_EXE_taskboard"))
            .env("TASKBOARD_FILE", &self.storage)
            .args(arguments)
            .output()
            .expect("taskboard process starts")
    }

    fn storage(&self) -> &Path {
        &self.storage
    }
}

impl Drop for Sandbox {
    fn drop(&mut self) {
        let _ignored = fs::remove_dir_all(&self.root);
    }
}

fn stdout(output: &Output) -> String {
    String::from_utf8(output.stdout.clone()).expect("stdout is UTF-8")
}

fn stderr(output: &Output) -> String {
    String::from_utf8(output.stderr.clone()).expect("stderr is UTF-8")
}

#[test]
fn command_sequence_persists_across_real_processes() {
    let sandbox = Sandbox::new();

    let added = sandbox.run(["add", "high", "Repair", "parser"]);
    assert!(added.status.success(), "{}", stderr(&added));
    assert_eq!(stdout(&added), "added task 1\n");

    let second = sandbox.run(["add", "normal", "Write", "tests"]);
    assert!(second.status.success(), "{}", stderr(&second));
    assert_eq!(stdout(&second), "added task 2\n");

    let started = sandbox.run(["start", "1"]);
    assert!(started.status.success(), "{}", stderr(&started));
    let completed = sandbox.run(["done", "1"]);
    assert!(completed.status.success(), "{}", stderr(&completed));

    let renamed = sandbox.run(["rename", "2", "Write", "integration", "tests"]);
    assert!(renamed.status.success(), "{}", stderr(&renamed));
    assert_eq!(stdout(&renamed), "renamed task 2\n");

    let listed = sandbox.run(["list"]);
    assert!(listed.status.success(), "{}", stderr(&listed));
    assert_eq!(
        stdout(&listed),
        concat!(
            "ID\tSTATUS\tPRIORITY\tTITLE\n",
            "1\tdone\thigh\tRepair parser\n",
            "2\ttodo\tnormal\tWrite integration tests\n",
        )
    );

    let stats = sandbox.run(["stats"]);
    assert!(stats.status.success(), "{}", stderr(&stats));
    assert_eq!(stdout(&stats), "todo\t1\ndoing\t0\ndone\t1\ntotal\t2\n");
}

#[test]
fn search_filter_remove_and_monotonic_ids_have_stable_behavior() {
    let sandbox = Sandbox::new();
    assert!(sandbox.run(["add", "high", "Repair", "Parser"]).status.success());
    assert!(sandbox.run(["add", "low", "Write", "parser", "guide"]).status.success());
    assert!(sandbox.run(["start", "2"]).status.success());

    let search = sandbox.run(["search", "PARSER"]);
    assert!(search.status.success(), "{}", stderr(&search));
    assert!(stdout(&search).contains("Repair Parser"));
    assert!(stdout(&search).contains("Write parser guide"));

    let doing = sandbox.run(["list", "doing"]);
    assert!(doing.status.success(), "{}", stderr(&doing));
    assert!(!stdout(&doing).contains("Repair Parser"));
    assert!(stdout(&doing).contains("Write parser guide"));

    assert!(sandbox.run(["remove", "1"]).status.success());
    let third = sandbox.run(["add", "normal", "Third"]);
    assert!(third.status.success(), "{}", stderr(&third));
    assert_eq!(stdout(&third), "added task 3\n");
}

#[test]
fn command_failures_use_exit_two_and_do_not_create_storage() {
    let sandbox = Sandbox::new();
    let output = sandbox.run(["add", "urgent", "Bad priority"]);
    assert_eq!(output.status.code(), Some(2));
    assert!(stderr(&output).contains("command error"));
    assert!(!sandbox.storage().exists());
}

#[test]
fn failed_domain_transition_preserves_existing_storage_bytes() {
    let sandbox = Sandbox::new();
    assert!(sandbox.run(["add", "normal", "Task"]).status.success());
    let before = fs::read(sandbox.storage()).expect("storage exists");

    let output = sandbox.run(["done", "1"]);
    assert_eq!(output.status.code(), Some(1));
    assert!(stderr(&output).contains("cannot complete task 1 from state todo"));
    let after = fs::read(sandbox.storage()).expect("storage remains");
    assert_eq!(before, after);
}

#[test]
fn rejected_rename_preserves_existing_storage_bytes() {
    let sandbox = Sandbox::new();
    assert!(sandbox.run(["add", "normal", "Original"]).status.success());
    let before = fs::read(sandbox.storage()).expect("storage exists");

    let output = sandbox.run(["rename", "1", "   "]);
    assert_eq!(output.status.code(), Some(1));
    assert!(stderr(&output).contains("task title cannot be empty"));
    let after = fs::read(sandbox.storage()).expect("storage remains");
    assert_eq!(before, after);
}

#[test]
fn malformed_storage_reports_the_record_line() {
    let sandbox = Sandbox::new();
    fs::write(
        sandbox.storage(),
        concat!(
            "TASKBOARD-V1\n",
            "NEXT_ID\t2\n",
            "TASK\t1\tflying\thigh\tBroken\n",
        ),
    )
    .expect("write malformed fixture");

    let output = sandbox.run(["list"]);
    assert_eq!(output.status.code(), Some(1));
    assert!(stderr(&output).contains("line 3"));
    assert!(stderr(&output).contains("invalid status"));
}

#[test]
fn help_and_version_do_not_touch_storage() {
    let sandbox = Sandbox::new();
    let help = sandbox.run(["help"]);
    assert!(help.status.success(), "{}", stderr(&help));
    assert!(stdout(&help).contains("USAGE:"));
    assert!(!sandbox.storage().exists());

    let version = sandbox.run(["version"]);
    assert!(version.status.success(), "{}", stderr(&version));
    assert!(stdout(&version).starts_with("taskboard "));
    assert!(!sandbox.storage().exists());
}
