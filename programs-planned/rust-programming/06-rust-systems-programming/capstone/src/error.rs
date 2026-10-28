
//! Application-level errors with preserved source causes.

use crate::domain::{ArchiveError, LogicalPathError};
use crate::path_policy::PathPolicyError;
use crate::process_capture::CaptureError;
use crate::store::StoreError;
use std::fmt;
use std::io;
use std::path::PathBuf;

#[derive(Debug)]
pub enum AppError {
    Usage(String),
    Io {
        operation: &'static str,
        path: PathBuf,
        source: io::Error,
    },
    NonUnicodeFileName(PathBuf),
    InvalidLogicalPath {
        input: String,
        source: LogicalPathError,
    },
    Archive(ArchiveError),
    Store(StoreError),
    Extraction(PathPolicyError),
    Capture(CaptureError),
}

impl AppError {
    pub fn usage(message: impl Into<String>) -> Self {
        Self::Usage(message.into())
    }

    pub fn io(
        operation: &'static str,
        path: impl Into<PathBuf>,
        source: io::Error,
    ) -> Self {
        Self::Io {
            operation,
            path: path.into(),
            source,
        }
    }

    #[must_use]
    pub const fn exit_code(&self) -> i32 {
        match self {
            Self::Usage(_) => 2,
            _ => 1,
        }
    }
}

impl fmt::Display for AppError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Usage(message) => formatter.write_str(message),
            Self::Io { operation, path, source } => {
                write!(formatter, "could not {operation} `{}`: {source}", path.display())
            }
            Self::NonUnicodeFileName(path) => write!(formatter, "source filename is not Unicode: {}", path.display()),
            Self::InvalidLogicalPath { input, source } => {
                write!(formatter, "invalid logical archive path `{input}`: {source}")
            }
            Self::Archive(error) => write!(formatter, "archive invariant failed: {error}"),
            Self::Store(error) => write!(formatter, "archive store failed: {error}"),
            Self::Extraction(error) => write!(formatter, "extraction failed: {error}"),
            Self::Capture(error) => write!(formatter, "process capture failed: {error}"),
        }
    }
}

impl std::error::Error for AppError {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            Self::Io { source, .. } => Some(source),
            Self::InvalidLogicalPath { source, .. } => Some(source),
            Self::Archive(error) => Some(error),
            Self::Store(error) => Some(error),
            Self::Extraction(error) => Some(error),
            Self::Capture(error) => Some(error),
            _ => None,
        }
    }
}

impl From<ArchiveError> for AppError {
    fn from(error: ArchiveError) -> Self {
        Self::Archive(error)
    }
}

impl From<StoreError> for AppError {
    fn from(error: StoreError) -> Self {
        Self::Store(error)
    }
}

impl From<PathPolicyError> for AppError {
    fn from(error: PathPolicyError) -> Self {
        Self::Extraction(error)
    }
}

impl From<CaptureError> for AppError {
    fn from(error: CaptureError) -> Self {
        Self::Capture(error)
    }
}
