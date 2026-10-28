use std::{fmt, io, path::PathBuf};

#[derive(Debug)]
pub enum StoreError {
    InvalidRecord(String),
    Validation {
        validator: &'static str,
        code: &'static str,
        message: String,
    },
    DuplicateValidator(&'static str),
    Capacity {
        limit: usize,
    },
    Format {
        offset: usize,
        message: String,
    },
    UnsupportedVersion(String),
    Checksum {
        expected: u32,
        actual: u32,
    },
    DuplicateKey(String),
    Migration {
        line: usize,
        message: String,
    },
    DestinationExists(PathBuf),
    UnsupportedPlatform(&'static str),
    Io {
        operation: &'static str,
        path: PathBuf,
        source: io::Error,
    },
    Durability {
        path: PathBuf,
        source: io::Error,
    },
    Usage(String),
}

impl StoreError {
    pub(crate) fn io(
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
}

impl fmt::Display for StoreError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::InvalidRecord(message) => write!(formatter, "invalid record: {message}"),
            Self::Validation {
                validator,
                code,
                message,
            } => write!(formatter, "validation {validator} ({code}): {message}"),
            Self::DuplicateValidator(name) => {
                write!(formatter, "duplicate validator name {name:?}")
            }
            Self::Capacity { limit } => {
                write!(formatter, "transaction capacity {limit} exceeded")
            }
            Self::Format { offset, message } => {
                write!(formatter, "archive byte {offset}: {message}")
            }
            Self::UnsupportedVersion(version) => {
                write!(formatter, "unsupported archive version {version}")
            }
            Self::Checksum { expected, actual } => write!(
                formatter,
                "checksum mismatch: expected {expected:#010x}, found {actual:#010x}"
            ),
            Self::DuplicateKey(key) => write!(formatter, "duplicate key {key:?}"),
            Self::Migration { line, message } => {
                write!(formatter, "legacy line {line}: {message}")
            }
            Self::DestinationExists(path) => {
                write!(formatter, "destination already exists: {}", path.display())
            }
            Self::UnsupportedPlatform(message) => formatter.write_str(message),
            Self::Io {
                operation,
                path,
                source,
            } => write!(formatter, "{operation} {}: {source}", path.display()),
            Self::Durability { path, source } => write!(
                formatter,
                "archive {} was installed, but parent-directory synchronization failed: {source}",
                path.display()
            ),
            Self::Usage(message) => formatter.write_str(message),
        }
    }
}

impl std::error::Error for StoreError {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            Self::Io { source, .. } | Self::Durability { source, .. } => Some(source),
            _ => None,
        }
    }
}
