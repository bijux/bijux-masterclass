#![forbid(unsafe_code)]

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Record {
    pub id: u64,
    pub amount: i64,
    pub note: Option<String>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Diagnostic {
    FieldCount { line: usize },
    InvalidId { line: usize, value: String },
    InvalidAmount { line: usize, value: String },
    InvalidNote { line: usize },
    DuplicateId { line: usize, id: u64 },
    TrimmedNote { line: usize },
}

impl Diagnostic {
    pub fn line(&self) -> usize {
        match self {
            Self::FieldCount { line }
            | Self::InvalidId { line, .. }
            | Self::InvalidAmount { line, .. }
            | Self::InvalidNote { line }
            | Self::DuplicateId { line, .. }
            | Self::TrimmedNote { line } => *line,
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Default)]
pub struct Batch<T, E> {
    pub accepted: Vec<T>,
    pub diagnostics: Vec<E>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Accepted<T, E> {
    pub line: usize,
    pub value: T,
    pub warnings: Vec<E>,
}

#[cfg(test)]
mod tests {
    use super::{Accepted, Batch, Diagnostic, Record};

    #[test]
    fn starter_distinguishes_accepted_values_from_diagnostics() {
        let batch = Batch {
            accepted: vec![Accepted {
                line: 2,
                value: Record { id: 7, amount: 3, note: None },
                warnings: vec![],
            }],
            diagnostics: vec![Diagnostic::FieldCount { line: 3 }],
        };
        assert_eq!(batch.accepted[0].line, 2);
        assert_eq!(batch.diagnostics.len(), 1);
    }
}
