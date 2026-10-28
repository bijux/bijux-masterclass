#![forbid(unsafe_code)]

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Diagnostic {
    MissingField,
    InvalidNumber,
}

impl Diagnostic {
    pub const fn code(self) -> u16 {
        match self {
            Self::MissingField => 1001,
            Self::InvalidNumber => 1002,
        }
    }
}
