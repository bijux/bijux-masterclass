//! Starter surface for the graceful task-tree laboratory.
//!
//! The starter defines terminal categories and the report shape. You still
//! need to build dynamic admission, child ownership, idempotent shutdown,
//! one-deadline draining, abort, complete joining, and paused-time tests.

use std::collections::BTreeMap;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Outcome {
    Completed,
    Failed(String),
    Panicked,
    Cancelled,
}

#[derive(Debug, Default, Clone, PartialEq, Eq)]
pub struct Report {
    pub outcomes: BTreeMap<String, Outcome>,
}

impl Report {
    pub fn total(&self) -> usize {
        self.outcomes.len()
    }

    pub fn count(&self, expected: &Outcome) -> usize {
        self.outcomes
            .values()
            .filter(|outcome| *outcome == expected)
            .count()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn report_uses_semantic_task_identity() {
        let mut report = Report::default();
        let _previous = report
            .outcomes
            .insert("index-refresh".to_owned(), Outcome::Completed);
        let _previous = report
            .outcomes
            .insert("metrics-flush".to_owned(), Outcome::Cancelled);

        assert_eq!(report.total(), 2);
        assert_eq!(report.outcomes["index-refresh"], Outcome::Completed);
    }
}
