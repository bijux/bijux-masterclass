use std::{fmt, io};

#[derive(Debug)]
pub enum ServiceError {
    Configuration(&'static str),
    Io(io::Error),
    Protocol(String),
    Timeout(&'static str),
    ConnectionClosed,
    Hyper(hyper::Error),
    Task(String),
}

impl fmt::Display for ServiceError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Configuration(field) => write!(f, "invalid configuration field: {field}"),
            Self::Io(error) => write!(f, "I/O failure: {error}"),
            Self::Protocol(message) => write!(f, "protocol failure: {message}"),
            Self::Timeout(stage) => write!(f, "deadline expired during {stage}"),
            Self::ConnectionClosed => f.write_str("peer closed the connection"),
            Self::Hyper(error) => write!(f, "HTTP connection failure: {error}"),
            Self::Task(message) => write!(f, "task failure: {message}"),
        }
    }
}

impl std::error::Error for ServiceError {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            Self::Io(error) => Some(error),
            Self::Hyper(error) => Some(error),
            _ => None,
        }
    }
}

impl From<io::Error> for ServiceError {
    fn from(value: io::Error) -> Self {
        Self::Io(value)
    }
}

impl From<hyper::Error> for ServiceError {
    fn from(value: hyper::Error) -> Self {
        Self::Hyper(value)
    }
}

#[derive(Debug)]
pub enum ClientError {
    Io(io::Error),
    Timeout(&'static str),
    Protocol(String),
    Rejected { code: String, message: String },
    Busy { retry_after_ms: u64 },
}

impl fmt::Display for ClientError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Io(error) => write!(f, "I/O failure: {error}"),
            Self::Timeout(stage) => write!(f, "timeout during {stage}"),
            Self::Protocol(message) => write!(f, "protocol failure: {message}"),
            Self::Rejected { code, message } => write!(f, "request rejected ({code}): {message}"),
            Self::Busy { retry_after_ms } => write!(f, "service busy; retry after {retry_after_ms} ms"),
        }
    }
}

impl std::error::Error for ClientError {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            Self::Io(error) => Some(error),
            _ => None,
        }
    }
}

impl From<io::Error> for ClientError {
    fn from(value: io::Error) -> Self {
        Self::Io(value)
    }
}
