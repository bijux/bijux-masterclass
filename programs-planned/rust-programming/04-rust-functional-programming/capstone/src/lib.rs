#![forbid(unsafe_code)]
#![doc = "LedgerFlow's deterministic transformation core."]

pub mod analysis;
pub mod app;
pub mod audit;
pub mod batch;
pub mod diagnostic;
pub mod domain;
pub mod ledger;
pub mod parse;
pub mod query;
pub mod report;

pub use analysis::{Analysis, analyze};
pub use app::{
    AppOutcome, Command, EXIT_COMMAND_ERROR, EXIT_DATA_ERROR, EXIT_OK, EXIT_USAGE,
    execute_text, parse_args,
};
pub use diagnostic::{Diagnostic, DiagnosticKind, Severity};
pub use domain::{AccountId, Event, EventId, EventKind};
pub use ledger::{AccountState, AccountStatus, Ledger};

/// Analyze a small valid source entirely in memory.
///
/// ```
/// use ledgerflow::analyze;
///
/// let source = "LEDGERFLOW-V1\n1\tacct-a\topen\t0\tstart\n";
/// let result = analyze(source);
/// assert_eq!(result.accepted().len(), 1);
/// assert!(!result.has_errors());
/// ```
pub fn analyze_example(source: &str) -> Analysis {
    analyze(source)
}
