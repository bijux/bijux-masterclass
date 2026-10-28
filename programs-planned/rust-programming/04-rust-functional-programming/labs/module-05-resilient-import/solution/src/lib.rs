#![forbid(unsafe_code)]

use std::collections::HashSet;

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

fn parse_note(line: usize, value: &str) -> Result<String, Diagnostic> {
    if value.chars().any(|character| character == '\0') {
        Err(Diagnostic::InvalidNote { line })
    } else {
        Ok(value.to_owned())
    }
}

pub fn parse_line(
    line: usize,
    text: &str,
) -> Result<Accepted<Record, Diagnostic>, Diagnostic> {
    let fields: Vec<_> = text.split('|').collect();
    if fields.len() != 3 {
        return Err(Diagnostic::FieldCount { line });
    }

    let id = fields[0]
        .parse()
        .map_err(|_| Diagnostic::InvalidId {
            line,
            value: fields[0].to_owned(),
        })?;
    let amount = fields[1]
        .parse()
        .map_err(|_| Diagnostic::InvalidAmount {
            line,
            value: fields[1].to_owned(),
        })?;

    let raw_note = fields[2];
    let trimmed_note = raw_note.trim();
    let note = (!trimmed_note.is_empty())
        .then_some(trimmed_note)
        .map(|value| parse_note(line, value))
        .transpose()?;
    let warnings = (raw_note != trimmed_note)
        .then(|| Diagnostic::TrimmedNote { line })
        .into_iter()
        .collect();

    Ok(Accepted {
        line,
        value: Record { id, amount, note },
        warnings,
    })
}

pub fn parse_all<'a, I>(
    lines: I,
) -> Result<Vec<Accepted<Record, Diagnostic>>, Diagnostic>
where
    I: IntoIterator<Item = &'a str>,
{
    lines
        .into_iter()
        .enumerate()
        .map(|(index, line)| parse_line(index + 1, line))
        .collect()
}

pub fn inspect_all<'a, I>(lines: I) -> Batch<Accepted<Record, Diagnostic>, Diagnostic>
where
    I: IntoIterator<Item = &'a str>,
{
    lines.into_iter().enumerate().fold(
        Batch::default(),
        |mut batch, (index, line)| {
            match parse_line(index + 1, line) {
                Ok(value) => batch.accepted.push(value),
                Err(error) => batch.diagnostics.push(error),
            }
            batch
        },
    )
}

pub fn reject_duplicates(
    mut batch: Batch<Accepted<Record, Diagnostic>, Diagnostic>,
) -> Batch<Accepted<Record, Diagnostic>, Diagnostic> {
    let mut seen = HashSet::new();
    let mut accepted = Vec::new();
    for item in batch.accepted {
        if seen.insert(item.value.id) {
            accepted.push(item);
        } else {
            batch.diagnostics.push(Diagnostic::DuplicateId {
                line: item.line,
                id: item.value.id,
            });
        }
    }
    batch.accepted = accepted;
    batch.diagnostics.sort_by_key(Diagnostic::line);
    batch
}

#[cfg(test)]
mod tests {
    use super::{Diagnostic, inspect_all, parse_all, parse_line, reject_duplicates};
    use std::cell::Cell;

    #[test]
    fn accepted_value_can_carry_a_warning() {
        let accepted = parse_line(1, "1|20| note ").unwrap();
        assert_eq!(accepted.value.note.as_deref(), Some("note"));
        assert_eq!(accepted.warnings, vec![Diagnostic::TrimmedNote { line: 1 }]);
    }

    #[test]
    fn optional_invalid_note_uses_transpose_to_keep_error() {
        assert_eq!(
            parse_line(3, "1|20|bad\0note"),
            Err(Diagnostic::InvalidNote { line: 3 })
        );
    }

    #[test]
    fn fail_fast_collection_does_not_visit_later_lines() {
        let calls = Cell::new(0);
        let lines = ["1|2|", "bad|3|", "4|5|"];
        let result: Result<Vec<_>, _> = lines
            .iter()
            .map(|line| {
                calls.set(calls.get() + 1);
                parse_line(calls.get(), line)
            })
            .collect();
        assert!(result.is_err());
        assert_eq!(calls.get(), 2);
        assert!(parse_all(lines).is_err());
    }

    #[test]
    fn inspection_accumulates_across_the_batch() {
        let batch = inspect_all(["1|2|", "bad|x|", "3|4|"]);
        assert_eq!(batch.accepted.len(), 2);
        assert_eq!(batch.diagnostics.len(), 1);
    }

    #[test]
    fn second_phase_diagnostics_merge_back_into_source_order() {
        let batch = reject_duplicates(inspect_all(["1|2|", "1|3|", "bad|4|"]));
        assert_eq!(
            batch.diagnostics,
            vec![
                Diagnostic::DuplicateId { line: 2, id: 1 },
                Diagnostic::InvalidId {
                    line: 3,
                    value: "bad".to_owned(),
                },
            ]
        );
    }

    #[test]
    fn duplicate_detection_is_a_second_phase_with_real_line_numbers() {
        let batch = reject_duplicates(inspect_all(["1|2|", "1|3|"]));
        assert_eq!(batch.accepted.len(), 1);
        assert_eq!(
            batch.diagnostics,
            vec![Diagnostic::DuplicateId { line: 2, id: 1 }]
        );
    }
}
