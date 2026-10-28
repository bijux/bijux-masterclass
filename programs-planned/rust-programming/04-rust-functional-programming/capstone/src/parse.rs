use crate::diagnostic::{Diagnostic, DiagnosticKind};
use crate::domain::{AccountId, Event, EventId, EventKind};
use std::str::FromStr;

pub const HEADER: &str = "LEDGERFLOW-V1";

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum RowInspection {
    Accepted {
        event: Event,
        warnings: Vec<Diagnostic>,
    },
    Rejected(Vec<Diagnostic>),
}

#[derive(Debug, Clone, PartialEq, Eq, Default)]
pub struct SourceInspection {
    prelude: Vec<Diagnostic>,
    rows: Vec<RowInspection>,
}

impl SourceInspection {
    pub fn prelude(&self) -> &[Diagnostic] {
        &self.prelude
    }

    pub fn rows(&self) -> &[RowInspection] {
        &self.rows
    }

    pub fn into_parts(self) -> (Vec<Diagnostic>, Vec<RowInspection>) {
        (self.prelude, self.rows)
    }
}

fn trimmed_warning(line: usize, field: &'static str, original: &str) -> Option<Diagnostic> {
    (original != original.trim()).then(|| {
        Diagnostic::warning(line, DiagnosticKind::FieldTrimmed { field })
    })
}

pub fn inspect_row(line: usize, text: &str) -> RowInspection {
    let fields: Vec<_> = text.split('\t').collect();
    if fields.len() != 5 {
        return RowInspection::Rejected(vec![Diagnostic::error(
            line,
            DiagnosticKind::FieldCount {
                expected: 5,
                found: fields.len(),
            },
        )]);
    }

    let mut errors = Vec::new();
    let mut warnings = Vec::new();

    let id_text = fields[0];
    let account_text = fields[1];
    let kind_text = fields[2];
    let amount_text = fields[3];
    let note_text = fields[4];

    for (name, value) in [
        ("event id", id_text),
        ("account id", account_text),
        ("event kind", kind_text),
        ("amount", amount_text),
        ("note", note_text),
    ] {
        if let Some(warning) = trimmed_warning(line, name, value) {
            warnings.push(warning);
        }
    }

    let id = match EventId::from_str(id_text.trim()) {
        Ok(value) => Some(value),
        Err(_) => {
            errors.push(Diagnostic::error(
                line,
                DiagnosticKind::InvalidEventId {
                    value: id_text.to_owned(),
                },
            ));
            None
        }
    };

    let account = match AccountId::parse(account_text) {
        Ok(value) => Some(value),
        Err(_) => {
            errors.push(Diagnostic::error(
                line,
                DiagnosticKind::InvalidAccount {
                    value: account_text.to_owned(),
                },
            ));
            None
        }
    };

    let kind = match EventKind::from_str(kind_text) {
        Ok(value) => Some(value),
        Err(_) => {
            errors.push(Diagnostic::error(
                line,
                DiagnosticKind::InvalidKind {
                    value: kind_text.to_owned(),
                },
            ));
            None
        }
    };

    let amount = match amount_text.trim().parse::<i64>() {
        Ok(value) => Some(value),
        Err(_) => {
            errors.push(Diagnostic::error(
                line,
                DiagnosticKind::InvalidAmount {
                    value: amount_text.to_owned(),
                },
            ));
            None
        }
    };

    match (id, account, kind, amount) {
        (Some(id), Some(account), Some(kind), Some(amount)) => {
            let note = (!note_text.trim().is_empty()).then(|| note_text.trim().to_owned());
            RowInspection::Accepted {
                event: Event::new(line, id, account, kind, amount, note),
                warnings,
            }
        }
        _ => RowInspection::Rejected(errors),
    }
}

pub fn inspect_source(input: &str) -> SourceInspection {
    let mut lines = input.lines().enumerate();
    let Some((header_index, header)) = lines.next() else {
        return SourceInspection {
            prelude: vec![Diagnostic::error(1, DiagnosticKind::MissingHeader)],
            rows: Vec::new(),
        };
    };

    if header != HEADER {
        return SourceInspection {
            prelude: vec![Diagnostic::error(
                header_index + 1,
                DiagnosticKind::UnsupportedHeader {
                    found: header.to_owned(),
                },
            )],
            rows: Vec::new(),
        };
    }

    let rows = lines
        .filter_map(|(index, line)| {
            let trimmed = line.trim();
            if trimmed.is_empty() || trimmed.starts_with('#') {
                None
            } else {
                Some(inspect_row(index + 1, line))
            }
        })
        .collect();

    SourceInspection {
        prelude: Vec::new(),
        rows,
    }
}

#[cfg(test)]
mod tests {
    use super::{RowInspection, inspect_row, inspect_source};
    use crate::diagnostic::{DiagnosticKind, Severity};

    #[test]
    fn row_accumulates_independent_field_errors() {
        let RowInspection::Rejected(diagnostics) = inspect_row(8, "zero\t\tunknown\tnan\tnote")
        else {
            panic!("row should be rejected");
        };
        assert_eq!(diagnostics.len(), 4);
        assert!(matches!(diagnostics[0].kind(), DiagnosticKind::InvalidEventId { .. }));
        assert!(matches!(diagnostics[1].kind(), DiagnosticKind::InvalidAccount { .. }));
        assert!(matches!(diagnostics[2].kind(), DiagnosticKind::InvalidKind { .. }));
        assert!(matches!(diagnostics[3].kind(), DiagnosticKind::InvalidAmount { .. }));
    }

    #[test]
    fn physical_line_numbers_survive_ignored_lines() {
        let source = "LEDGERFLOW-V1\n\n# comment\n1\tacct\topen\t0\tstart\n";
        let inspection = inspect_source(source);
        let RowInspection::Accepted { event, .. } = &inspection.rows()[0] else {
            panic!("event should parse");
        };
        assert_eq!(event.line(), 4);
    }

    #[test]
    fn trimming_is_a_warning_not_a_rejection() {
        let RowInspection::Accepted { warnings, .. } =
            inspect_row(2, " 1 \t acct \t open \t 0 \t note ")
        else {
            panic!("event should parse");
        };
        assert_eq!(warnings.len(), 5);
        assert!(warnings.iter().all(|item| item.severity() == Severity::Warning));
    }

    #[test]
    fn unsupported_header_stops_untrusted_row_decoding() {
        let inspection = inspect_source("OTHER\n1\ta\topen\t0\tx\n");
        assert_eq!(inspection.prelude().len(), 1);
        assert!(inspection.rows().is_empty());
    }
}
