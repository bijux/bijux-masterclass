use crate::{ArgError, Diagnostic};
use std::error::Error;
use std::fmt;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum CommandError {
    Arguments(ArgError),
    Domain(String),
}

impl From<ArgError> for CommandError {
    fn from(error: ArgError) -> Self { Self::Arguments(error) }
}

impl fmt::Display for CommandError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Arguments(error) => write!(formatter, "{}: {error}", Diagnostic::ArgumentFailure),
            Self::Domain(message) => write!(formatter, "{}: {message}", Diagnostic::DomainFailure),
        }
    }
}

impl Error for CommandError {
    fn source(&self) -> Option<&(dyn Error + 'static)> {
        match self { Self::Arguments(error) => Some(error), Self::Domain(_) => None }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum AppError {
    Usage(String),
    UnknownCommand(String),
    Command(CommandError),
}

impl fmt::Display for AppError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Usage(message) => write!(formatter, "{}: {message}", Diagnostic::UsageFailure),
            Self::UnknownCommand(name) => write!(formatter, "{}: `{name}`", Diagnostic::UnknownCommand),
            Self::Command(error) => error.fmt(formatter),
        }
    }
}

impl Error for AppError {
    fn source(&self) -> Option<&(dyn Error + 'static)> {
        match self { Self::Command(error) => Some(error), _ => None }
    }
}
