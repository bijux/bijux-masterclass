use crate::metrics::MetricsSnapshot;
use std::collections::BTreeMap;
use std::fmt;
use std::num::NonZeroUsize;
use std::str::FromStr;

pub const MANIFEST_HEADER: &str = "BATCHWEAVE-V1";
pub const MAX_JOBS: usize = 4096;
pub const MAX_ID_BYTES: usize = 64;
pub const MAX_PAYLOAD_BYTES: usize = 64 * 1024;
pub const MAX_TOTAL_PAYLOAD_BYTES: usize = 8 * 1024 * 1024;
pub const MAX_WORKERS: usize = 64;
pub const MAX_QUEUE_CAPACITY: usize = 4096;
pub const MAX_REPORT_THREADS: usize = 64;

#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct JobId(String);

impl JobId {
    pub fn new(value: impl Into<String>) -> Result<Self, &'static str> {
        let value = value.into();
        if value.is_empty() {
            return Err("job id is empty");
        }
        if value.len() > MAX_ID_BYTES {
            return Err("job id is too long");
        }
        if value.bytes().any(|byte| byte.is_ascii_control() || byte == b'\t') {
            return Err("job id contains a control character");
        }
        Ok(Self(value))
    }

    #[must_use]
    pub fn as_str(&self) -> &str {
        &self.0
    }
}

impl fmt::Display for JobId {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        formatter.write_str(&self.0)
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub enum Operation {
    Checksum,
    WordCount,
    SortIntegers,
    PrimeCount,
    Panic,
}

impl Operation {
    #[must_use]
    pub const fn as_str(self) -> &'static str {
        match self {
            Self::Checksum => "checksum",
            Self::WordCount => "word-count",
            Self::SortIntegers => "sort-integers",
            Self::PrimeCount => "prime-count",
            Self::Panic => "panic",
        }
    }
}

impl fmt::Display for Operation {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        formatter.write_str(self.as_str())
    }
}

impl FromStr for Operation {
    type Err = &'static str;

    fn from_str(value: &str) -> Result<Self, Self::Err> {
        match value {
            "checksum" => Ok(Self::Checksum),
            "word-count" => Ok(Self::WordCount),
            "sort-integers" => Ok(Self::SortIntegers),
            "prime-count" => Ok(Self::PrimeCount),
            "panic" => Ok(Self::Panic),
            _ => Err("unsupported operation"),
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Job {
    pub index: usize,
    pub id: JobId,
    pub operation: Operation,
    pub payload: String,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum FailurePolicy {
    Continue,
    FailFast,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum OutcomeKind {
    Completed(String),
    DomainFailed(String),
    Panicked,
    Cancelled,
}

impl OutcomeKind {
    #[must_use]
    pub const fn status(&self) -> &'static str {
        match self {
            Self::Completed(_) => "completed",
            Self::DomainFailed(_) => "failed",
            Self::Panicked => "panicked",
            Self::Cancelled => "cancelled",
        }
    }

    #[must_use]
    pub fn detail(&self) -> &str {
        match self {
            Self::Completed(value) | Self::DomainFailed(value) => value,
            Self::Panicked => "worker panicked while executing the job",
            Self::Cancelled => "job was cancelled before completion",
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct JobOutcome {
    pub index: usize,
    pub id: JobId,
    pub operation: Operation,
    pub kind: OutcomeKind,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Summary {
    pub total: usize,
    pub by_status: BTreeMap<String, usize>,
    pub by_operation: BTreeMap<String, usize>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RunReport {
    pub outcomes: Vec<JobOutcome>,
    pub summary: Summary,
    pub live_metrics_at_end: MetricsSnapshot,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct EngineConfig {
    pub workers: NonZeroUsize,
    pub queue_capacity: NonZeroUsize,
    pub report_threads: NonZeroUsize,
    pub failure_policy: FailurePolicy,
}

impl EngineConfig {
    pub fn new(
        workers: usize,
        queue_capacity: usize,
        report_threads: usize,
        failure_policy: FailurePolicy,
    ) -> Result<Self, &'static str> {
        let workers = NonZeroUsize::new(workers).ok_or("workers must be nonzero")?;
        let queue_capacity =
            NonZeroUsize::new(queue_capacity).ok_or("queue capacity must be nonzero")?;
        let report_threads =
            NonZeroUsize::new(report_threads).ok_or("report threads must be nonzero")?;
        if workers.get() > MAX_WORKERS {
            return Err("worker count exceeds the course product limit");
        }
        if queue_capacity.get() > MAX_QUEUE_CAPACITY {
            return Err("queue capacity exceeds the course product limit");
        }
        if report_threads.get() > MAX_REPORT_THREADS {
            return Err("report thread count exceeds the course product limit");
        }
        Ok(Self {
            workers,
            queue_capacity,
            report_threads,
            failure_policy,
        })
    }
}

impl Default for EngineConfig {
    fn default() -> Self {
        // The single-threaded default is deliberately conservative. The CLI
        // selects a wider default explicitly, where invalid configuration can
        // be reported to the caller rather than hidden behind a panic.
        Self {
            workers: NonZeroUsize::MIN,
            queue_capacity: NonZeroUsize::MIN,
            report_threads: NonZeroUsize::MIN,
            failure_policy: FailurePolicy::Continue,
        }
    }
}
