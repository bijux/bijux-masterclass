//! Reference implementation for an in-memory aggregate over `Vec<Task>`.

use std::error::Error;
use std::fmt;

/// Nonzero task identifier.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, PartialOrd, Ord)]
pub struct TaskId(u64);

impl TaskId {
    /// Returns the primitive value.
    pub const fn get(self) -> u64 {
        self.0
    }
}

impl fmt::Display for TaskId {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        self.0.fmt(formatter)
    }
}

/// Lifecycle state of one task.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Status {
    /// Not started.
    Todo,
    /// Active.
    Doing,
    /// Complete.
    Done,
}

/// Operation applied to a task.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Operation {
    /// `Todo -> Doing`.
    Start,
    /// `Doing -> Done`.
    Complete,
    /// `Done -> Todo`.
    Reopen,
}

/// One board-owned task.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Task {
    id: TaskId,
    title: String,
    status: Status,
}

impl Task {
    fn new(id: TaskId, title: String) -> Self {
        Self { id, title, status: Status::Todo }
    }

    /// Returns the stable ID.
    pub const fn id(&self) -> TaskId {
        self.id
    }

    /// Borrows the owned title.
    pub fn title(&self) -> &str {
        &self.title
    }

    /// Returns current state.
    pub const fn status(&self) -> Status {
        self.status
    }

    fn apply(&mut self, operation: Operation) -> bool {
        let next = match (self.status, operation) {
            (Status::Todo, Operation::Start) => Status::Doing,
            (Status::Doing, Operation::Complete) => Status::Done,
            (Status::Done, Operation::Reopen) => Status::Todo,
            _ => return false,
        };
        self.status = next;
        true
    }
}

/// Aggregate operation failure.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum BoardError {
    /// No identifier remains.
    IdExhausted,
    /// Title was empty after trimming.
    EmptyTitle,
    /// No task has the requested ID.
    NotFound(TaskId),
    /// Task exists but cannot perform the requested transition.
    IllegalTransition {
        /// Affected task.
        id: TaskId,
        /// State that rejected the operation.
        from: Status,
        /// Requested operation.
        operation: Operation,
    },
}

impl fmt::Display for BoardError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::IdExhausted => write!(formatter, "task ID space is exhausted"),
            Self::EmptyTitle => write!(formatter, "task title cannot be empty"),
            Self::NotFound(id) => write!(formatter, "task {id} was not found"),
            Self::IllegalTransition { id, from, operation } => {
                write!(formatter, "task {id} in state {from:?} cannot perform {operation:?}")
            }
        }
    }
}

impl Error for BoardError {}

/// Deterministic status counts.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)]
pub struct StatusCounts {
    /// Number of todo tasks.
    pub todo: usize,
    /// Number of doing tasks.
    pub doing: usize,
    /// Number of done tasks.
    pub done: usize,
}

impl StatusCounts {
    /// Renders fields in stable lifecycle order.
    pub fn render(self) -> String {
        format!(
            "todo: {}\ndoing: {}\ndone: {}\ntotal: {}",
            self.todo,
            self.doing,
            self.done,
            self.todo + self.doing + self.done
        )
    }
}

/// Owner of task storage and ID allocation.
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
    /// Creates an empty board whose first ID is one.
    pub const fn new() -> Self {
        Self { tasks: Vec::new(), next_id: Some(1) }
    }

    /// Adds an owned title and returns its allocated ID.
    pub fn add(&mut self, title: String) -> Result<TaskId, BoardError> {
        if title.trim().is_empty() {
            return Err(BoardError::EmptyTitle);
        }
        let raw = self.next_id.ok_or(BoardError::IdExhausted)?;
        let id = TaskId(raw);
        self.next_id = raw.checked_add(1);
        self.tasks.push(Task::new(id, title));
        Ok(id)
    }

    /// Borrows all tasks in insertion order.
    pub fn tasks(&self) -> &[Task] {
        &self.tasks
    }

    /// Borrows a task by ID.
    pub fn find(&self, id: TaskId) -> Option<&Task> {
        self.tasks.iter().find(|task| task.id == id)
    }

    /// Mutably borrows a task by ID without exposing collection structure.
    pub fn find_mut(&mut self, id: TaskId) -> Option<&mut Task> {
        self.tasks.iter_mut().find(|task| task.id == id)
    }

    /// Applies one typed transition.
    pub fn transition(&mut self, id: TaskId, operation: Operation) -> Result<(), BoardError> {
        let task = self.find_mut(id).ok_or(BoardError::NotFound(id))?;
        let from = task.status;
        if task.apply(operation) {
            Ok(())
        } else {
            Err(BoardError::IllegalTransition { id, from, operation })
        }
    }

    /// Removes and returns a task while preserving relative order of survivors.
    pub fn remove(&mut self, id: TaskId) -> Result<Task, BoardError> {
        let index = self
            .tasks
            .iter()
            .position(|task| task.id == id)
            .ok_or(BoardError::NotFound(id))?;
        Ok(self.tasks.remove(index))
    }

    /// Iterates over one status without allocating a result collection.
    pub fn by_status(&self, status: Status) -> impl Iterator<Item = &Task> {
        self.tasks.iter().filter(move |task| task.status == status)
    }

    /// Searches titles with ASCII case folding and borrows matching tasks.
    pub fn search(&self, query: &str) -> impl Iterator<Item = &Task> {
        let query = query.to_ascii_lowercase();
        self.tasks.iter().filter(move |task| task.title.to_ascii_lowercase().contains(&query))
    }

    /// Counts tasks by status.
    pub fn counts(&self) -> StatusCounts {
        let mut counts = StatusCounts::default();
        for task in &self.tasks {
            match task.status {
                Status::Todo => counts.todo += 1,
                Status::Doing => counts.doing += 1,
                Status::Done => counts.done += 1,
            }
        }
        counts
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn empty_board_has_stable_views() {
        let board = TaskBoard::new();
        assert!(board.tasks().is_empty());
        assert_eq!(board.counts(), StatusCounts::default());
        assert_eq!(board.counts().render(), "todo: 0\ndoing: 0\ndone: 0\ntotal: 0");
    }

    #[test]
    fn ids_are_monotonic_and_not_reused() {
        let mut board = TaskBoard::new();
        let first = board.add(String::from("first")).expect("valid");
        let second = board.add(String::from("second")).expect("valid");
        board.remove(first).expect("exists");
        let third = board.add(String::from("third")).expect("valid");
        assert_eq!((first.get(), second.get(), third.get()), (1, 2, 3));
        assert_eq!(
            board
                .tasks()
                .iter()
                .map(|task| task.title())
                .collect::<Vec<_>>(),
            vec!["second", "third"]
        );
    }

    #[test]
    fn failed_transition_preserves_state() {
        let mut board = TaskBoard::new();
        let id = board.add(String::from("task")).expect("valid");
        let error = board.transition(id, Operation::Complete).expect_err("todo cannot complete");
        assert!(matches!(error, BoardError::IllegalTransition { from: Status::Todo, .. }));
        assert_eq!(board.find(id).map(Task::status), Some(Status::Todo));
    }

    #[test]
    fn legal_cycle_and_counts_are_explicit() {
        let mut board = TaskBoard::new();
        let first = board.add(String::from("Parser")).expect("valid");
        let second = board.add(String::from("Tests")).expect("valid");
        board.transition(first, Operation::Start).expect("legal");
        board.transition(first, Operation::Complete).expect("legal");
        assert_eq!(board.by_status(Status::Done).map(Task::id).collect::<Vec<_>>(), vec![first]);
        assert_eq!(board.counts(), StatusCounts { todo: 1, doing: 0, done: 1 });
        assert_eq!(board.search("par").map(Task::id).collect::<Vec<_>>(), vec![first]);
        assert_eq!(board.search("TEST").map(Task::id).collect::<Vec<_>>(), vec![second]);
    }

    #[test]
    fn exhaustion_is_reported_without_wraparound() {
        let mut board = TaskBoard { tasks: Vec::new(), next_id: Some(u64::MAX) };
        let last = board.add(String::from("last")).expect("maximum ID is still valid");
        assert_eq!(last.get(), u64::MAX);
        assert_eq!(board.add(String::from("overflow")), Err(BoardError::IdExhausted));
    }
}
