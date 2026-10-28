use std::collections::HashSet;
use std::error::Error;
use std::fmt;
use std::str::FromStr;

pub(crate) const MAX_TITLE_BYTES: usize = 120;

/// Stable, nonzero identifier allocated by a [`TaskBoard`].
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, PartialOrd, Ord)]
pub struct TaskId(u64);

impl TaskId {
    /// Constructs an identifier when `value` is nonzero.
    pub const fn new(value: u64) -> Option<Self> {
        if value == 0 {
            None
        } else {
            Some(Self(value))
        }
    }

    /// Returns the primitive identifier value.
    pub const fn get(self) -> u64 {
        self.0
    }
}

impl fmt::Display for TaskId {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        self.0.fmt(formatter)
    }
}

/// Failure to parse a nonzero task identifier.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ParseTaskIdError {
    input: String,
}

impl fmt::Display for ParseTaskIdError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(formatter, "invalid nonzero task ID `{}`", self.input)
    }
}

impl Error for ParseTaskIdError {}

impl FromStr for TaskId {
    type Err = ParseTaskIdError;

    fn from_str(input: &str) -> Result<Self, Self::Err> {
        input
            .parse::<u64>()
            .ok()
            .and_then(Self::new)
            .ok_or_else(|| ParseTaskIdError {
                input: input.to_owned(),
            })
    }
}

/// Scheduling importance attached to a task.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, PartialOrd, Ord)]
pub enum Priority {
    /// Work that can wait behind ordinary tasks.
    Low,
    /// Default scheduling importance.
    Normal,
    /// Work that should be considered before lower-priority tasks.
    High,
}

impl fmt::Display for Priority {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        let text = match self {
            Self::Low => "low",
            Self::Normal => "normal",
            Self::High => "high",
        };
        formatter.write_str(text)
    }
}

/// Failure to parse a supported task priority.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ParsePriorityError {
    input: String,
}

impl fmt::Display for ParsePriorityError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(
            formatter,
            "invalid priority `{}`; expected low, normal, or high",
            self.input
        )
    }
}

impl Error for ParsePriorityError {}

impl FromStr for Priority {
    type Err = ParsePriorityError;

    fn from_str(input: &str) -> Result<Self, Self::Err> {
        match input {
            "low" => Ok(Self::Low),
            "normal" => Ok(Self::Normal),
            "high" => Ok(Self::High),
            _ => Err(ParsePriorityError {
                input: input.to_owned(),
            }),
        }
    }
}

/// Complete lifecycle state of a task.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, PartialOrd, Ord)]
pub enum Status {
    /// Task has not been started.
    Todo,
    /// Task is currently being worked on.
    Doing,
    /// Task has been completed.
    Done,
}

impl fmt::Display for Status {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        let text = match self {
            Self::Todo => "todo",
            Self::Doing => "doing",
            Self::Done => "done",
        };
        formatter.write_str(text)
    }
}

/// Failure to parse a supported task status.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ParseStatusError {
    input: String,
}

impl fmt::Display for ParseStatusError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(
            formatter,
            "invalid status `{}`; expected todo, doing, or done",
            self.input
        )
    }
}

impl Error for ParseStatusError {}

impl FromStr for Status {
    type Err = ParseStatusError;

    fn from_str(input: &str) -> Result<Self, Self::Err> {
        match input {
            "todo" => Ok(Self::Todo),
            "doing" => Ok(Self::Doing),
            "done" => Ok(Self::Done),
            _ => Err(ParseStatusError {
                input: input.to_owned(),
            }),
        }
    }
}

/// One task owned by a [`TaskBoard`].
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Task {
    id: TaskId,
    title: String,
    priority: Priority,
    status: Status,
}

impl Task {
    pub(crate) fn restore(
        id: TaskId,
        title: String,
        priority: Priority,
        status: Status,
    ) -> Result<Self, TaskError> {
        validate_title(&title)?;
        Ok(Self {
            id,
            title,
            priority,
            status,
        })
    }

    /// Returns the stable identifier.
    pub const fn id(&self) -> TaskId {
        self.id
    }

    /// Borrows the owned title.
    pub fn title(&self) -> &str {
        &self.title
    }

    /// Returns scheduling priority.
    pub const fn priority(&self) -> Priority {
        self.priority
    }

    /// Returns current lifecycle state.
    pub const fn status(&self) -> Status {
        self.status
    }
}

/// Domain invariant or lifecycle transition failure.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum TaskError {
    /// A title was empty or contained only whitespace.
    EmptyTitle,
    /// A title exceeded the storage protocol's byte limit.
    TitleTooLong {
        /// Observed UTF-8 byte length.
        bytes: usize,
        /// Maximum accepted UTF-8 byte length.
        maximum: usize,
    },
    /// A title contained a tab or line break and could not be serialized safely.
    InvalidTitleCharacter,
    /// No further `u64` identifier can be allocated.
    IdExhausted,
    /// No task has the requested identifier.
    NotFound(TaskId),
    /// The requested lifecycle operation is invalid from the current state.
    IllegalTransition {
        /// Affected task.
        id: TaskId,
        /// Requested operation.
        operation: &'static str,
        /// State from which the operation was attempted.
        from: Status,
    },
    /// A restored snapshot contains the same ID more than once.
    DuplicateId(TaskId),
    /// Restored allocation metadata would reuse or skip backward across an ID.
    InvalidNextId,
}

impl fmt::Display for TaskError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::EmptyTitle => formatter.write_str("task title cannot be empty"),
            Self::TitleTooLong { bytes, maximum } => {
                write!(formatter, "task title is {bytes} bytes; maximum is {maximum}")
            }
            Self::InvalidTitleCharacter => {
                formatter.write_str("task title cannot contain tab or line breaks")
            }
            Self::IdExhausted => formatter.write_str("task ID space is exhausted"),
            Self::NotFound(id) => write!(formatter, "task {id} was not found"),
            Self::IllegalTransition {
                id,
                operation,
                from,
            } => write!(
                formatter,
                "cannot {operation} task {id} from state {from}"
            ),
            Self::DuplicateId(id) => write!(formatter, "duplicate task ID {id}"),
            Self::InvalidNextId => {
                formatter.write_str("restored next ID is inconsistent with stored task IDs")
            }
        }
    }
}

impl Error for TaskError {}

/// Deterministic count of tasks in every lifecycle state.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)]
pub struct Stats {
    /// Number of not-started tasks.
    pub todo: usize,
    /// Number of active tasks.
    pub doing: usize,
    /// Number of completed tasks.
    pub done: usize,
}

impl Stats {
    /// Returns the number of all retained tasks.
    pub const fn total(self) -> usize {
        self.todo + self.doing + self.done
    }
}

/// Aggregate root that owns tasks and monotonic ID allocation state.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct TaskBoard {
    tasks: Vec<Task>,
    next_id: Option<u64>,
}

impl Default for TaskBoard {
    fn default() -> Self {
        Self::new()
    }
}

impl TaskBoard {
    /// Constructs an empty board whose first allocated ID is one.
    pub const fn new() -> Self {
        Self {
            tasks: Vec::new(),
            next_id: Some(1),
        }
    }

    pub(crate) fn restore(
        mut tasks: Vec<Task>,
        next_id: Option<u64>,
    ) -> Result<Self, TaskError> {
        let mut seen = HashSet::new();
        let mut maximum = 0_u64;

        for task in &tasks {
            if !seen.insert(task.id) {
                return Err(TaskError::DuplicateId(task.id));
            }
            maximum = maximum.max(task.id.get());
        }

        match next_id {
            Some(value) if value != 0 && value > maximum => {}
            None if maximum == u64::MAX => {}
            _ => return Err(TaskError::InvalidNextId),
        }

        tasks.sort_unstable_by_key(Task::id);
        Ok(Self { tasks, next_id })
    }

    pub(crate) const fn next_id_token(&self) -> Option<u64> {
        self.next_id
    }

    /// Borrows all retained tasks in ascending ID order.
    pub fn tasks(&self) -> &[Task] {
        &self.tasks
    }

    /// Adds a validated task in the `todo` state and returns its new ID.
    pub fn add(&mut self, priority: Priority, title: String) -> Result<TaskId, TaskError> {
        validate_title(&title)?;
        let raw_id = self.next_id.ok_or(TaskError::IdExhausted)?;
        let id = TaskId(raw_id);
        self.next_id = raw_id.checked_add(1);
        self.tasks.push(Task {
            id,
            title,
            priority,
            status: Status::Todo,
        });
        Ok(id)
    }

    /// Borrows one task by ID.
    pub fn find(&self, id: TaskId) -> Option<&Task> {
        self.tasks.iter().find(|task| task.id == id)
    }

    fn find_mut(&mut self, id: TaskId) -> Result<&mut Task, TaskError> {
        self.tasks
            .iter_mut()
            .find(|task| task.id == id)
            .ok_or(TaskError::NotFound(id))
    }

    /// Moves a task from `todo` to `doing`.
    pub fn start(&mut self, id: TaskId) -> Result<(), TaskError> {
        let task = self.find_mut(id)?;
        if task.status != Status::Todo {
            return Err(TaskError::IllegalTransition {
                id,
                operation: "start",
                from: task.status,
            });
        }
        task.status = Status::Doing;
        Ok(())
    }

    /// Moves a task from `doing` to `done`.
    pub fn complete(&mut self, id: TaskId) -> Result<(), TaskError> {
        let task = self.find_mut(id)?;
        if task.status != Status::Doing {
            return Err(TaskError::IllegalTransition {
                id,
                operation: "complete",
                from: task.status,
            });
        }
        task.status = Status::Done;
        Ok(())
    }

    /// Moves a task from `done` back to `todo`.
    pub fn reopen(&mut self, id: TaskId) -> Result<(), TaskError> {
        let task = self.find_mut(id)?;
        if task.status != Status::Done {
            return Err(TaskError::IllegalTransition {
                id,
                operation: "reopen",
                from: task.status,
            });
        }
        task.status = Status::Todo;
        Ok(())
    }

    /// Replaces a task title after validating the complete title contract.
    ///
    /// Validation happens before a mutable task borrow is taken, so a rejected
    /// title leaves the board byte-for-byte equivalent at the model boundary.
    pub fn rename(&mut self, id: TaskId, title: String) -> Result<(), TaskError> {
        validate_title(&title)?;
        let task = self.find_mut(id)?;
        task.title = title;
        Ok(())
    }

    /// Removes a task and transfers ownership of it to the caller.
    pub fn remove(&mut self, id: TaskId) -> Result<Task, TaskError> {
        let index = self
            .tasks
            .iter()
            .position(|task| task.id == id)
            .ok_or(TaskError::NotFound(id))?;
        Ok(self.tasks.remove(index))
    }

    /// Iterates over all tasks or only tasks matching `status`.
    pub fn filtered(&self, status: Option<Status>) -> impl Iterator<Item = &Task> {
        self.tasks
            .iter()
            .filter(move |task| status.is_none_or(|expected| task.status == expected))
    }

    /// Searches titles with documented ASCII case-insensitive semantics.
    pub fn search(&self, query: &str) -> impl Iterator<Item = &Task> {
        let normalized = query.to_ascii_lowercase();
        self.tasks.iter().filter(move |task| {
            task.title
                .to_ascii_lowercase()
                .contains(normalized.as_str())
        })
    }

    /// Counts retained tasks by lifecycle state.
    pub fn stats(&self) -> Stats {
        let mut stats = Stats::default();
        for task in &self.tasks {
            match task.status {
                Status::Todo => stats.todo += 1,
                Status::Doing => stats.doing += 1,
                Status::Done => stats.done += 1,
            }
        }
        stats
    }
}

fn validate_title(title: &str) -> Result<(), TaskError> {
    if title.trim().is_empty() {
        return Err(TaskError::EmptyTitle);
    }
    if title.len() > MAX_TITLE_BYTES {
        return Err(TaskError::TitleTooLong {
            bytes: title.len(),
            maximum: MAX_TITLE_BYTES,
        });
    }
    if title
        .chars()
        .any(|character| matches!(character, '\t' | '\n' | '\r'))
    {
        return Err(TaskError::InvalidTitleCharacter);
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    fn id(value: u64) -> TaskId {
        TaskId::new(value).expect("test IDs are nonzero")
    }

    #[test]
    fn identifiers_reject_zero_and_non_numeric_input() {
        assert_eq!(TaskId::new(0), None);
        assert!("0".parse::<TaskId>().is_err());
        assert!("abc".parse::<TaskId>().is_err());
        assert_eq!("42".parse::<TaskId>().map(TaskId::get), Ok(42));
    }

    #[test]
    fn priority_and_status_round_trip_through_text() {
        for priority in [Priority::Low, Priority::Normal, Priority::High] {
            assert_eq!(priority.to_string().parse::<Priority>(), Ok(priority));
        }
        for status in [Status::Todo, Status::Doing, Status::Done] {
            assert_eq!(status.to_string().parse::<Status>(), Ok(status));
        }
    }

    #[test]
    fn rename_reuses_title_validation_and_is_failure_atomic() {
        let mut board = TaskBoard::new();
        let task_id = board
            .add(Priority::Normal, String::from("Original"))
            .expect("valid task");

        board
            .rename(task_id, String::from("Revised title"))
            .expect("valid rename");
        assert_eq!(board.find(task_id).map(Task::title), Some("Revised title"));

        assert_eq!(
            board.rename(task_id, String::from("   ")),
            Err(TaskError::EmptyTitle)
        );
        assert_eq!(board.find(task_id).map(Task::title), Some("Revised title"));
        assert_eq!(
            board.rename(id(99), String::from("Valid title")),
            Err(TaskError::NotFound(id(99)))
        );
    }

    #[test]
    fn title_contract_rejects_blank_oversized_and_delimited_text() {
        let mut board = TaskBoard::new();
        assert_eq!(
            board.add(Priority::Low, String::from("   ")),
            Err(TaskError::EmptyTitle)
        );
        assert!(matches!(
            board.add(Priority::Low, "x".repeat(MAX_TITLE_BYTES + 1)),
            Err(TaskError::TitleTooLong { .. })
        ));
        assert_eq!(
            board.add(Priority::Low, String::from("bad\ttitle")),
            Err(TaskError::InvalidTitleCharacter)
        );
    }

    #[test]
    fn lifecycle_is_explicit_and_rejects_skipped_transitions() {
        let mut board = TaskBoard::new();
        let task_id = board
            .add(Priority::High, String::from("Repair parser"))
            .expect("valid task");

        assert!(matches!(
            board.complete(task_id),
            Err(TaskError::IllegalTransition {
                from: Status::Todo,
                ..
            })
        ));
        board.start(task_id).expect("todo may start");
        board.complete(task_id).expect("doing may complete");
        board.reopen(task_id).expect("done may reopen");
        assert_eq!(board.find(task_id).map(Task::status), Some(Status::Todo));
    }

    #[test]
    fn removed_identifiers_are_not_reused() {
        let mut board = TaskBoard::new();
        let first = board
            .add(Priority::Low, String::from("First"))
            .expect("valid task");
        board.remove(first).expect("task exists");
        let second = board
            .add(Priority::Low, String::from("Second"))
            .expect("valid task");
        assert_eq!(second.get(), 2);
    }

    #[test]
    fn restore_rejects_duplicate_and_backward_allocation_metadata() {
        let task = Task::restore(
            id(7),
            String::from("Stored"),
            Priority::Normal,
            Status::Todo,
        )
        .expect("valid stored task");
        assert_eq!(
            TaskBoard::restore(vec![task.clone(), task], Some(8)),
            Err(TaskError::DuplicateId(id(7)))
        );

        let task = Task::restore(
            id(7),
            String::from("Stored"),
            Priority::Normal,
            Status::Todo,
        )
        .expect("valid stored task");
        assert_eq!(
            TaskBoard::restore(vec![task], Some(7)),
            Err(TaskError::InvalidNextId)
        );
    }

    #[test]
    fn filtering_searching_and_statistics_borrow_the_board() {
        let mut board = TaskBoard::new();
        let first = board
            .add(Priority::High, String::from("Repair Parser"))
            .expect("valid task");
        let second = board
            .add(Priority::Normal, String::from("Write tests"))
            .expect("valid task");
        board.start(first).expect("todo may start");
        board.start(second).expect("todo may start");
        board.complete(second).expect("doing may complete");

        let doing: Vec<_> = board.filtered(Some(Status::Doing)).map(Task::id).collect();
        assert_eq!(doing, vec![first]);
        assert_eq!(board.search("parser").count(), 1);
        assert_eq!(
            board.stats(),
            Stats {
                todo: 0,
                doing: 1,
                done: 1,
            }
        );
    }
}
