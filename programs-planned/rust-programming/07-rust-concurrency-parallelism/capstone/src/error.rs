use std::fmt;
use std::io;

#[derive(Debug)]
pub enum ManifestError {
    Empty,
    InvalidHeader { found: String },
    TooManyJobs { count: usize, limit: usize },
    MalformedLine { line: usize, message: String },
    DuplicateId { line: usize, id: String },
    PayloadTooLarge { line: usize, count: usize, limit: usize },
    TotalPayloadTooLarge { line: usize, count: usize, limit: usize },
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum DomainError {
    InvalidInteger { token: String },
    TooManyIntegers { count: usize, limit: usize },
    PrimeLimitInvalid { value: String },
    PrimeLimitTooLarge { value: u64, limit: u64 },
}

#[derive(Debug)]
pub enum RunError {
    InvalidConfiguration(String),
    InvalidJobIndex { position: usize, observed: usize },
    DuplicateJobId(String),
    DuplicateOutcome { index: usize },
    OutcomeOutOfRange { index: usize, count: usize },
    ThreadSpawn { worker: usize, message: String },
    WorkerPanicked { worker: usize },
    MissingOutcome { index: usize },
    ReportPool(String),
}

#[derive(Debug)]
pub enum AppError {
    Usage(String),
    Io { path: String, source: io::Error },
    Manifest(ManifestError),
    Run(RunError),
}

impl fmt::Display for ManifestError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Empty => write!(f, "manifest is empty"),
            Self::InvalidHeader { found } => write!(f, "expected BATCHWEAVE-V1 header, found {found:?}"),
            Self::TooManyJobs { count, limit } => write!(f, "manifest contains {count} jobs; limit is {limit}"),
            Self::MalformedLine { line, message } => write!(f, "manifest line {line}: {message}"),
            Self::DuplicateId { line, id } => write!(f, "manifest line {line}: duplicate job id {id:?}"),
            Self::PayloadTooLarge { line, count, limit } => write!(f, "manifest line {line}: payload has {count} bytes; limit is {limit}"),
            Self::TotalPayloadTooLarge { line, count, limit } => write!(f, "manifest line {line}: cumulative payload is {count} bytes; limit is {limit}"),
        }
    }
}

impl fmt::Display for DomainError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::InvalidInteger { token } => write!(f, "invalid signed integer {token:?}"),
            Self::TooManyIntegers { count, limit } => write!(f, "integer list has {count} items; limit is {limit}"),
            Self::PrimeLimitInvalid { value } => write!(f, "invalid prime-count limit {value:?}"),
            Self::PrimeLimitTooLarge { value, limit } => write!(f, "prime-count limit {value} exceeds {limit}"),
        }
    }
}

impl fmt::Display for RunError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::InvalidConfiguration(message) => write!(f, "invalid engine configuration: {message}"),
            Self::InvalidJobIndex { position, observed } => write!(f, "job at position {position} has index {observed}"),
            Self::DuplicateJobId(id) => write!(f, "duplicate job id {id:?}"),
            Self::DuplicateOutcome { index } => write!(f, "worker protocol produced duplicate outcome index {index}"),
            Self::OutcomeOutOfRange { index, count } => write!(f, "worker protocol produced outcome index {index} for {count} jobs"),
            Self::ThreadSpawn { worker, message } => write!(f, "could not spawn worker {worker}: {message}"),
            Self::WorkerPanicked { worker } => write!(f, "worker {worker} panicked outside the contained job boundary"),
            Self::MissingOutcome { index } => write!(f, "no terminal outcome exists for job index {index}"),
            Self::ReportPool(message) => write!(f, "could not build report pool: {message}"),
        }
    }
}

impl fmt::Display for AppError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Usage(message) => f.write_str(message),
            Self::Io { path, source } => write!(f, "could not read {path:?}: {source}"),
            Self::Manifest(error) => write!(f, "{error}"),
            Self::Run(error) => write!(f, "{error}"),
        }
    }
}

impl std::error::Error for ManifestError {}
impl std::error::Error for DomainError {}
impl std::error::Error for RunError {}
impl std::error::Error for AppError {}

impl From<ManifestError> for AppError {
    fn from(value: ManifestError) -> Self { Self::Manifest(value) }
}
impl From<RunError> for AppError {
    fn from(value: RunError) -> Self { Self::Run(value) }
}
