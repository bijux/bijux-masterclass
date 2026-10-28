use crate::{
    Command, CommandParseError, HELP, Status, StorageError, Task, TaskBoard, TaskError,
    load_path, parse_command, save_path,
};
use std::error::Error;
use std::fmt;
use std::path::Path;

/// Result of executing one typed command against an in-memory board.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Outcome {
    output: String,
    changed: bool,
}

impl Outcome {
    fn read_only(output: String) -> Self {
        Self {
            output,
            changed: false,
        }
    }

    fn changed(output: String) -> Self {
        Self {
            output,
            changed: true,
        }
    }

    /// Borrows user-facing standard output.
    pub fn output(&self) -> &str {
        &self.output
    }

    /// Reports whether successful execution changed persistent state.
    pub const fn changed_state(&self) -> bool {
        self.changed
    }

    /// Transfers owned output to the caller.
    pub fn into_output(self) -> String {
        self.output
    }
}

/// Failure at one of the command, storage, or domain application boundaries.
#[derive(Debug)]
pub enum RunError {
    /// Raw command-line tokens did not satisfy the grammar.
    Command(CommandParseError),
    /// Loading or committing persistent state failed.
    Storage(StorageError),
    /// A requested task operation violated a domain rule.
    Task(TaskError),
}

impl RunError {
    /// Returns the command-line exit status assigned to this failure category.
    pub const fn exit_code(&self) -> i32 {
        match self {
            Self::Command(_) => 2,
            Self::Storage(_) | Self::Task(_) => 1,
        }
    }
}

impl fmt::Display for RunError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Command(error) => write!(formatter, "command error: {error}"),
            Self::Storage(error) => write!(formatter, "storage error: {error}"),
            Self::Task(error) => write!(formatter, "task error: {error}"),
        }
    }
}

impl Error for RunError {
    fn source(&self) -> Option<&(dyn Error + 'static)> {
        match self {
            Self::Command(error) => Some(error),
            Self::Storage(error) => Some(error),
            Self::Task(error) => Some(error),
        }
    }
}

impl From<CommandParseError> for RunError {
    fn from(error: CommandParseError) -> Self {
        Self::Command(error)
    }
}

impl From<StorageError> for RunError {
    fn from(error: StorageError) -> Self {
        Self::Storage(error)
    }
}

impl From<TaskError> for RunError {
    fn from(error: TaskError) -> Self {
        Self::Task(error)
    }
}

/// Executes one typed command without performing path I/O.
pub fn execute(board: &mut TaskBoard, command: Command) -> Result<Outcome, TaskError> {
    match command {
        Command::Add { priority, title } => {
            let id = board.add(priority, title)?;
            Ok(Outcome::changed(format!("added task {id}\n")))
        }
        Command::List { status } => Ok(Outcome::read_only(render_tasks(board, status))),
        Command::Start(id) => {
            board.start(id)?;
            Ok(Outcome::changed(format!("started task {id}\n")))
        }
        Command::Done(id) => {
            board.complete(id)?;
            Ok(Outcome::changed(format!("completed task {id}\n")))
        }
        Command::Reopen(id) => {
            board.reopen(id)?;
            Ok(Outcome::changed(format!("reopened task {id}\n")))
        }
        Command::Remove(id) => {
            let removed = board.remove(id)?;
            Ok(Outcome::changed(format!(
                "removed task {}: {}\n",
                removed.id(),
                removed.title()
            )))
        }
        Command::Rename { id, title } => {
            board.rename(id, title)?;
            Ok(Outcome::changed(format!("renamed task {id}\n")))
        }
        Command::Search(query) => {
            let tasks: Vec<&Task> = board.search(&query).collect();
            Ok(Outcome::read_only(render_task_slice(&tasks)))
        }
        Command::Stats => Ok(Outcome::read_only(render_stats(board))),
        Command::Help => Ok(Outcome::read_only(HELP.to_owned())),
        Command::Version => Ok(Outcome::read_only(format!(
            "taskboard {}\n",
            env!("CARGO_PKG_VERSION")
        ))),
    }
}

/// Parses, loads, executes, conditionally commits, and returns standard output.
///
/// Help and version are handled before loading. Mutating command output is
/// returned only after the required save succeeds.
pub fn run(arguments: &[String], path: &Path) -> Result<String, RunError> {
    let command = parse_command(arguments)?;

    if matches!(command, Command::Help | Command::Version) {
        return execute(&mut TaskBoard::new(), command)
            .map(Outcome::into_output)
            .map_err(RunError::from);
    }

    let mut board = load_path(path)?;
    let outcome = execute(&mut board, command)?;
    if outcome.changed_state() {
        save_path(path, &board)?;
    }
    Ok(outcome.into_output())
}

fn render_tasks(board: &TaskBoard, status: Option<Status>) -> String {
    let tasks: Vec<&Task> = board.filtered(status).collect();
    render_task_slice(&tasks)
}

fn render_task_slice(tasks: &[&Task]) -> String {
    if tasks.is_empty() {
        return String::from("no tasks\n");
    }

    let mut output = String::from("ID\tSTATUS\tPRIORITY\tTITLE\n");
    for task in tasks {
        output.push_str(&format!(
            "{}\t{}\t{}\t{}\n",
            task.id(),
            task.status(),
            task.priority(),
            task.title()
        ));
    }
    output
}

fn render_stats(board: &TaskBoard) -> String {
    let stats = board.stats();
    format!(
        "todo\t{}\ndoing\t{}\ndone\t{}\ntotal\t{}\n",
        stats.todo,
        stats.doing,
        stats.done,
        stats.total()
    )
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::{Priority, TaskId};

    fn id(value: u64) -> TaskId {
        TaskId::new(value).expect("test ID is nonzero")
    }

    #[test]
    fn mutating_outcomes_are_marked_only_after_successful_execution() {
        let mut board = TaskBoard::new();
        let added = execute(
            &mut board,
            Command::Add {
                priority: Priority::High,
                title: String::from("Repair parser"),
            },
        )
        .expect("valid add");
        assert!(added.changed_state());

        let failure = execute(&mut board, Command::Done(id(1)));
        assert!(failure.is_err());
        assert_eq!(board.find(id(1)).map(Task::status), Some(Status::Todo));
    }

    #[test]
    fn list_and_search_use_the_same_deterministic_table_contract() {
        let mut board = TaskBoard::new();
        board
            .add(Priority::High, String::from("Repair Parser"))
            .expect("valid task");
        board
            .add(Priority::Low, String::from("Write guide"))
            .expect("valid task");

        let listed = execute(&mut board, Command::List { status: None })
            .expect("list succeeds")
            .into_output();
        assert_eq!(
            listed,
            concat!(
                "ID\tSTATUS\tPRIORITY\tTITLE\n",
                "1\ttodo\thigh\tRepair Parser\n",
                "2\ttodo\tlow\tWrite guide\n",
            )
        );

        let searched = execute(&mut board, Command::Search(String::from("parser")))
            .expect("search succeeds")
            .into_output();
        assert_eq!(
            searched,
            concat!(
                "ID\tSTATUS\tPRIORITY\tTITLE\n",
                "1\ttodo\thigh\tRepair Parser\n",
            )
        );
    }

    #[test]
    fn rename_changes_state_only_after_domain_validation() {
        let mut board = TaskBoard::new();
        let task_id = board
            .add(Priority::Normal, String::from("Original"))
            .expect("valid task");

        let outcome = execute(
            &mut board,
            Command::Rename {
                id: task_id,
                title: String::from("Revised"),
            },
        )
        .expect("valid rename");
        assert!(outcome.changed_state());
        assert_eq!(outcome.output(), "renamed task 1\n");
        assert_eq!(board.find(task_id).map(Task::title), Some("Revised"));

        let failed = execute(
            &mut board,
            Command::Rename {
                id: task_id,
                title: String::from("   "),
            },
        );
        assert!(matches!(failed, Err(TaskError::EmptyTitle)));
        assert_eq!(board.find(task_id).map(Task::title), Some("Revised"));
    }

    #[test]
    fn empty_results_and_stats_have_stable_output() {
        let mut board = TaskBoard::new();
        assert_eq!(
            execute(&mut board, Command::List { status: None })
                .expect("list succeeds")
                .output(),
            "no tasks\n"
        );
        assert_eq!(
            execute(&mut board, Command::Stats)
                .expect("stats succeeds")
                .output(),
            "todo\t0\ndoing\t0\ndone\t0\ntotal\t0\n"
        );
    }
}
