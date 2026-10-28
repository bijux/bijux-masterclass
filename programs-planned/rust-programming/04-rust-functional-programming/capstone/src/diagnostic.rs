use crate::domain::{AccountId, EventId, EventKind};
use std::fmt;

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum Severity {
    Warning,
    Error,
}

impl Severity {
    pub fn as_str(self) -> &'static str {
        match self {
            Self::Warning => "warning",
            Self::Error => "error",
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum DiagnosticKind {
    MissingHeader,
    UnsupportedHeader { found: String },
    FieldCount { expected: usize, found: usize },
    InvalidEventId { value: String },
    InvalidAccount { value: String },
    InvalidKind { value: String },
    InvalidAmount { value: String },
    FieldTrimmed { field: &'static str },
    DuplicateEventId {
        id: EventId,
        first_line: usize,
    },
    LifecycleAmountMustBeZero { kind: EventKind, amount: i64 },
    TransferAmountMustBePositive { kind: EventKind, amount: i64 },
    AccountAlreadyExists { account: AccountId },
    AccountNotFound { account: AccountId },
    AccountClosed { account: AccountId },
    InsufficientFunds {
        account: AccountId,
        available: i64,
        requested: i64,
    },
    BalanceMustBeZeroToClose { account: AccountId, balance: i64 },
    BalanceOverflow { account: AccountId },
}

impl DiagnosticKind {
    pub fn code(&self) -> &'static str {
        match self {
            Self::MissingHeader => "LF001",
            Self::UnsupportedHeader { .. } => "LF002",
            Self::FieldCount { .. } => "LF003",
            Self::InvalidEventId { .. } => "LF004",
            Self::InvalidAccount { .. } => "LF005",
            Self::InvalidKind { .. } => "LF006",
            Self::InvalidAmount { .. } => "LF007",
            Self::FieldTrimmed { .. } => "LF101",
            Self::DuplicateEventId { .. } => "LF008",
            Self::LifecycleAmountMustBeZero { .. } => "LF009",
            Self::TransferAmountMustBePositive { .. } => "LF010",
            Self::AccountAlreadyExists { .. } => "LF011",
            Self::AccountNotFound { .. } => "LF012",
            Self::AccountClosed { .. } => "LF013",
            Self::InsufficientFunds { .. } => "LF014",
            Self::BalanceMustBeZeroToClose { .. } => "LF015",
            Self::BalanceOverflow { .. } => "LF016",
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Diagnostic {
    line: usize,
    severity: Severity,
    kind: DiagnosticKind,
}

impl Diagnostic {
    pub fn error(line: usize, kind: DiagnosticKind) -> Self {
        Self {
            line,
            severity: Severity::Error,
            kind,
        }
    }

    pub fn warning(line: usize, kind: DiagnosticKind) -> Self {
        Self {
            line,
            severity: Severity::Warning,
            kind,
        }
    }

    pub fn line(&self) -> usize {
        self.line
    }

    pub fn severity(&self) -> Severity {
        self.severity
    }

    pub fn kind(&self) -> &DiagnosticKind {
        &self.kind
    }

    pub fn code(&self) -> &'static str {
        self.kind.code()
    }

    pub fn is_error(&self) -> bool {
        self.severity == Severity::Error
    }
}

impl fmt::Display for Diagnostic {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(
            formatter,
            "{}\t{}\tline {}\t",
            self.severity.as_str(),
            self.code(),
            self.line
        )?;
        match &self.kind {
            DiagnosticKind::MissingHeader => {
                formatter.write_str("missing LEDGERFLOW-V1 header")
            }
            DiagnosticKind::UnsupportedHeader { found } => {
                write!(formatter, "unsupported header {found:?}")
            }
            DiagnosticKind::FieldCount { expected, found } => write!(
                formatter,
                "expected {expected} tab-separated fields, found {found}"
            ),
            DiagnosticKind::InvalidEventId { value } => {
                write!(formatter, "invalid nonzero event id {value:?}")
            }
            DiagnosticKind::InvalidAccount { value } => {
                write!(formatter, "invalid account id {value:?}")
            }
            DiagnosticKind::InvalidKind { value } => {
                write!(formatter, "invalid event kind {value:?}")
            }
            DiagnosticKind::InvalidAmount { value } => {
                write!(formatter, "invalid signed-cent amount {value:?}")
            }
            DiagnosticKind::FieldTrimmed { field } => {
                write!(formatter, "surrounding whitespace was removed from {field}")
            }
            DiagnosticKind::DuplicateEventId { id, first_line } => write!(
                formatter,
                "event id {id} was first declared on line {first_line}"
            ),
            DiagnosticKind::LifecycleAmountMustBeZero { kind, amount } => write!(
                formatter,
                "{kind} requires amount 0, found {amount}"
            ),
            DiagnosticKind::TransferAmountMustBePositive { kind, amount } => write!(
                formatter,
                "{kind} requires a positive amount, found {amount}"
            ),
            DiagnosticKind::AccountAlreadyExists { account } => {
                write!(formatter, "account {account} already exists")
            }
            DiagnosticKind::AccountNotFound { account } => {
                write!(formatter, "account {account} has not been opened")
            }
            DiagnosticKind::AccountClosed { account } => {
                write!(formatter, "account {account} is closed")
            }
            DiagnosticKind::InsufficientFunds {
                account,
                available,
                requested,
            } => write!(
                formatter,
                "account {account} has {available} cents, cannot withdraw {requested}"
            ),
            DiagnosticKind::BalanceMustBeZeroToClose { account, balance } => write!(
                formatter,
                "account {account} has balance {balance}; close requires zero"
            ),
            DiagnosticKind::BalanceOverflow { account } => {
                write!(formatter, "balance arithmetic overflow for account {account}")
            }
        }
    }
}
