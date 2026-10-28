use std::error::Error;
use std::fmt;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct ArgumentSpec {
    pub flag: &'static str,
    pub help: &'static str,
    pub required: bool,
}

pub trait CommandArgs: Sized {
    const USAGE: &'static str;
    const ARGUMENTS: &'static [ArgumentSpec];
    fn decode(raw: &[String]) -> Result<Self, ArgError>;
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ArgError {
    UnknownArgument { flag: String },
    DuplicateArgument { flag: &'static str },
    MissingValue { flag: &'static str },
    MissingRequired { flag: &'static str },
    InvalidValue {
        flag: &'static str,
        value: String,
        message: String,
    },
    InvalidDefault {
        flag: &'static str,
        value: &'static str,
        message: String,
    },
}

impl fmt::Display for ArgError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::UnknownArgument { flag } => write!(formatter, "unknown argument `{flag}`"),
            Self::DuplicateArgument { flag } => write!(formatter, "argument `{flag}` was supplied more than once"),
            Self::MissingValue { flag } => write!(formatter, "argument `{flag}` requires a value"),
            Self::MissingRequired { flag } => write!(formatter, "required argument `{flag}` is missing"),
            Self::InvalidValue { flag, value, message } => {
                write!(formatter, "invalid value `{value}` for `{flag}`: {message}")
            }
            Self::InvalidDefault { flag, value, message } => {
                write!(formatter, "invalid generated default `{value}` for `{flag}`: {message}")
            }
        }
    }
}

impl Error for ArgError {}
