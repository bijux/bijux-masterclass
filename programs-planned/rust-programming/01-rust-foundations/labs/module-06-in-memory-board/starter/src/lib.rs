//! Read-only baseline for the in-memory task-board laboratory.
//!
//! Allocation, lifecycle transitions, search, removal, and counts remain the
//! learner's work. The supplied types establish only private ownership and views.

/// Stable task identity.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, PartialOrd, Ord)]
pub struct TaskId(u64);

impl TaskId {
    /// Constructs a nonzero identity.
    pub const fn new(value: u64) -> Option<Self> {
        if value == 0 {
            None
        } else {
            Some(Self(value))
        }
    }

    /// Returns the primitive value.
    pub const fn get(self) -> u64 {
        self.0
    }
}

/// Minimal owned task record used by the starter's read-only view.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Task {
    id: TaskId,
    title: String,
}

impl Task {
    /// Borrows the title.
    pub fn title(&self) -> &str {
        &self.title
    }

    /// Returns task identity.
    pub const fn id(&self) -> TaskId {
        self.id
    }
}

/// Empty board shell whose mutation policy is intentionally unspecified.
#[derive(Debug, Default)]
pub struct TaskBoard {
    tasks: Vec<Task>,
}

impl TaskBoard {
    /// Creates an empty board.
    pub const fn new() -> Self {
        Self { tasks: Vec::new() }
    }

    /// Borrows all tasks in stable storage order.
    pub fn tasks(&self) -> &[Task] {
        &self.tasks
    }

    /// Returns the number of live tasks.
    pub fn len(&self) -> usize {
        self.tasks.len()
    }

    /// Reports whether no task is live.
    pub fn is_empty(&self) -> bool {
        self.tasks.is_empty()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn baseline_empty_view_is_stable() {
        let board = TaskBoard::new();
        assert!(board.is_empty());
        assert_eq!(board.len(), 0);
        assert_eq!(board.tasks(), []);
    }
}
