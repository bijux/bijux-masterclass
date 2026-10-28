use std::fmt;
use std::str::FromStr;

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct EventId(u64);

impl EventId {
    pub fn new(value: u64) -> Option<Self> {
        (value != 0).then_some(Self(value))
    }

    pub fn get(self) -> u64 {
        self.0
    }
}

impl fmt::Display for EventId {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(formatter, "{}", self.0)
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct EventIdParseError;

impl FromStr for EventId {
    type Err = EventIdParseError;

    fn from_str(value: &str) -> Result<Self, Self::Err> {
        value
            .parse::<u64>()
            .ok()
            .and_then(Self::new)
            .ok_or(EventIdParseError)
    }
}

#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct AccountId(String);

impl AccountId {
    pub fn parse(value: &str) -> Result<Self, AccountIdError> {
        let trimmed = value.trim();
        if trimmed.is_empty() {
            return Err(AccountIdError::Empty);
        }
        if trimmed.chars().any(|character| {
            character == '\t' || character == '\n' || character == '\r'
        }) {
            return Err(AccountIdError::ControlCharacter);
        }
        Ok(Self(trimmed.to_owned()))
    }

    pub fn as_str(&self) -> &str {
        &self.0
    }
}

impl fmt::Display for AccountId {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        formatter.write_str(&self.0)
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum AccountIdError {
    Empty,
    ControlCharacter,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum EventKind {
    Open,
    Deposit,
    Withdraw,
    Close,
}

impl EventKind {
    pub fn as_str(self) -> &'static str {
        match self {
            Self::Open => "open",
            Self::Deposit => "deposit",
            Self::Withdraw => "withdraw",
            Self::Close => "close",
        }
    }
}

impl fmt::Display for EventKind {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        formatter.write_str(self.as_str())
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct EventKindParseError;

impl FromStr for EventKind {
    type Err = EventKindParseError;

    fn from_str(value: &str) -> Result<Self, Self::Err> {
        match value.trim().to_ascii_lowercase().as_str() {
            "open" => Ok(Self::Open),
            "deposit" => Ok(Self::Deposit),
            "withdraw" => Ok(Self::Withdraw),
            "close" => Ok(Self::Close),
            _ => Err(EventKindParseError),
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Event {
    line: usize,
    id: EventId,
    account: AccountId,
    kind: EventKind,
    amount: i64,
    note: Option<String>,
}

impl Event {
    pub fn new(
        line: usize,
        id: EventId,
        account: AccountId,
        kind: EventKind,
        amount: i64,
        note: Option<String>,
    ) -> Self {
        Self {
            line,
            id,
            account,
            kind,
            amount,
            note,
        }
    }

    pub fn line(&self) -> usize {
        self.line
    }

    pub fn id(&self) -> EventId {
        self.id
    }

    pub fn account(&self) -> &AccountId {
        &self.account
    }

    pub fn kind(&self) -> EventKind {
        self.kind
    }

    pub fn amount(&self) -> i64 {
        self.amount
    }

    pub fn note(&self) -> Option<&str> {
        self.note.as_deref()
    }
}
