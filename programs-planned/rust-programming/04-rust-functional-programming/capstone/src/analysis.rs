use crate::audit::{AuditEntry, AuditTrail};
use crate::diagnostic::{Diagnostic, DiagnosticKind, Severity};
use crate::domain::{Event, EventId};
use crate::ledger::Ledger;
use crate::parse::{RowInspection, inspect_source};
use std::collections::BTreeMap;

#[derive(Debug, Clone)]
pub struct Analysis {
    ledger: Ledger,
    accepted: Vec<Event>,
    diagnostics: Vec<Diagnostic>,
    audit: AuditTrail,
    inspected_rows: usize,
}

impl Analysis {
    pub fn ledger(&self) -> &Ledger {
        &self.ledger
    }

    pub fn accepted(&self) -> &[Event] {
        &self.accepted
    }

    pub fn diagnostics(&self) -> &[Diagnostic] {
        &self.diagnostics
    }

    pub fn audit(&self) -> &AuditTrail {
        &self.audit
    }

    pub fn inspected_rows(&self) -> usize {
        self.inspected_rows
    }

    pub fn has_errors(&self) -> bool {
        self.diagnostics.iter().any(Diagnostic::is_error)
    }

    pub fn error_count(&self) -> usize {
        self.diagnostics
            .iter()
            .filter(|item| item.severity() == Severity::Error)
            .count()
    }

    pub fn warning_count(&self) -> usize {
        self.diagnostics
            .iter()
            .filter(|item| item.severity() == Severity::Warning)
            .count()
    }
}

pub fn analyze(input: &str) -> Analysis {
    let inspection = inspect_source(input);
    let (mut diagnostics, rows) = inspection.into_parts();
    let inspected_rows = rows.len();
    let mut ledger = Ledger::default();
    let mut accepted = Vec::new();
    let mut audit = AuditTrail::default();
    let mut seen: BTreeMap<EventId, usize> = BTreeMap::new();

    for row in rows {
        match row {
            RowInspection::Rejected(row_diagnostics) => {
                debug_assert!(
                    !row_diagnostics.is_empty(),
                    "row rejection must contain a diagnostic"
                );
                let Some(primary) = row_diagnostics.first() else {
                    // Keep the analyzer total if the parser's internal invariant
                    // is changed in a future revision.
                    continue;
                };
                audit = audit.push(AuditEntry::rejected(
                    primary.line(),
                    None,
                    None,
                    primary.code(),
                ));
                diagnostics.extend(row_diagnostics);
            }
            RowInspection::Accepted { event, warnings } => {
                diagnostics.extend(warnings);
                if let Some(first_line) = seen.get(&event.id()).copied() {
                    let diagnostic = Diagnostic::error(
                        event.line(),
                        DiagnosticKind::DuplicateEventId {
                            id: event.id(),
                            first_line,
                        },
                    );
                    audit = audit.push(AuditEntry::rejected(
                        event.line(),
                        Some(event.id()),
                        Some(event.account().clone()),
                        diagnostic.code(),
                    ));
                    diagnostics.push(diagnostic);
                    continue;
                }
                seen.insert(event.id(), event.line());

                match ledger.apply(&event) {
                    Ok(next) => {
                        ledger = next;
                        audit = audit.push(AuditEntry::accepted(
                            event.line(),
                            event.id(),
                            event.account().clone(),
                        ));
                        accepted.push(event);
                    }
                    Err(failure) => {
                        let (recovered, diagnostic) = failure.into_parts();
                        ledger = recovered;
                        audit = audit.push(AuditEntry::rejected(
                            event.line(),
                            Some(event.id()),
                            Some(event.account().clone()),
                            diagnostic.code(),
                        ));
                        diagnostics.push(diagnostic);
                    }
                }
            }
        }
    }

    Analysis {
        ledger,
        accepted,
        diagnostics,
        audit,
        inspected_rows,
    }
}

#[cfg(test)]
mod tests {
    use super::analyze;
    use crate::diagnostic::DiagnosticKind;
    use crate::domain::AccountId;

    #[test]
    fn independent_rows_and_state_failures_accumulate_in_source_order() {
        let source = concat!(
            "LEDGERFLOW-V1\n",
            "1\ta\topen\t0\tstart\n",
            "bad\ta\tdeposit\tx\tbroken\n",
            "2\ta\twithdraw\t4\ttoo early\n",
            "3\ta\tdeposit\t9\tok\n",
        );
        let analysis = analyze(source);
        assert_eq!(analysis.accepted().len(), 2);
        assert_eq!(analysis.diagnostics().len(), 3);
        assert_eq!(analysis.diagnostics()[0].line(), 3);
        assert_eq!(analysis.diagnostics()[1].line(), 3);
        assert_eq!(analysis.diagnostics()[2].line(), 4);
        let account = analysis
            .ledger()
            .get(&AccountId::parse("a").unwrap())
            .unwrap();
        assert_eq!(account.balance(), 9);
    }

    #[test]
    fn duplicate_identity_is_reserved_before_transition() {
        let source = concat!(
            "LEDGERFLOW-V1\n",
            "1\ta\tdeposit\t5\taccount missing\n",
            "1\ta\topen\t0\tduplicate id\n",
        );
        let analysis = analyze(source);
        assert!(analysis.accepted().is_empty());
        assert!(matches!(
            analysis.diagnostics()[1].kind(),
            DiagnosticKind::DuplicateEventId { first_line: 2, .. }
        ));
    }

    #[test]
    fn every_inspected_row_produces_exactly_one_audit_entry() {
        let source = concat!(
            "LEDGERFLOW-V1\n",
            "bad\ta\topen\tx\tbroken\n",
            "1\ta\topen\t0\taccepted\n",
            "2\ta\twithdraw\t1\trejected\n",
        );
        let analysis = analyze(source);
        assert_eq!(analysis.inspected_rows(), 3);
        assert_eq!(analysis.audit().len(), analysis.inspected_rows());
    }

    #[test]
    fn rejected_withdrawal_does_not_change_following_state() {
        let source = concat!(
            "LEDGERFLOW-V1\n",
            "1\ta\topen\t0\tstart\n",
            "2\ta\tdeposit\t5\tfund\n",
            "3\ta\twithdraw\t8\treject\n",
            "4\ta\twithdraw\t5\taccept\n",
            "5\ta\tclose\t0\tdone\n",
        );
        let analysis = analyze(source);
        assert_eq!(analysis.accepted().len(), 4);
        assert_eq!(analysis.error_count(), 1);
        assert_eq!(
            analysis
                .ledger()
                .get(&AccountId::parse("a").unwrap())
                .unwrap()
                .balance(),
            0
        );
    }
}
