#![forbid(unsafe_code)]

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum TaskMode { Normal, DomainFail, Panic, Spin(usize) }

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Task { pub index: usize, pub text: String, pub mode: TaskMode }

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum TaskOutcome {
    Completed { index: usize, value: String },
    Failed { index: usize, message: String },
    Panicked { index: usize },
    Cancelled { index: usize },
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum FailurePolicy { Continue, FailFast }

#[cfg(test)]
mod tests {
    use super::{FailurePolicy, TaskMode};
    #[test]
    fn baseline_protocol_is_typed() {
        assert_ne!(FailurePolicy::Continue, FailurePolicy::FailFast);
        assert!(matches!(TaskMode::Spin(3), TaskMode::Spin(3)));
    }
}
