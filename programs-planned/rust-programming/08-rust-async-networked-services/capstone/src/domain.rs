use std::{fmt, str::FromStr, time::Duration};

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum Operation {
    Uppercase,
    WordCount,
    Checksum,
    SleepMs,
}

impl Operation {
    pub const ALL: [Self; 4] = [
        Self::Uppercase,
        Self::WordCount,
        Self::Checksum,
        Self::SleepMs,
    ];

    pub const fn as_str(self) -> &'static str {
        match self {
            Self::Uppercase => "uppercase",
            Self::WordCount => "word-count",
            Self::Checksum => "checksum",
            Self::SleepMs => "sleep-ms",
        }
    }
}

impl fmt::Display for Operation {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str(self.as_str())
    }
}

impl FromStr for Operation {
    type Err = &'static str;

    fn from_str(value: &str) -> Result<Self, Self::Err> {
        match value {
            "uppercase" => Ok(Self::Uppercase),
            "word-count" => Ok(Self::WordCount),
            "checksum" => Ok(Self::Checksum),
            "sleep-ms" => Ok(Self::SleepMs),
            _ => Err("unsupported operation"),
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct JobRequest {
    pub idempotency_key: String,
    pub operation: Operation,
    pub payload: String,
}

impl JobRequest {
    pub fn fingerprint(&self) -> String {
        format!("{}\0{}", self.operation.as_str(), self.payload)
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct JobResult {
    pub value: String,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum HealthState {
    Starting,
    Ready,
    ShuttingDown,
    Failed,
}

impl HealthState {
    pub const fn as_str(self) -> &'static str {
        match self {
            Self::Starting => "starting",
            Self::Ready => "ready",
            Self::ShuttingDown => "shutting-down",
            Self::Failed => "failed",
        }
    }
}

impl FromStr for HealthState {
    type Err = &'static str;

    fn from_str(value: &str) -> Result<Self, Self::Err> {
        match value {
            "starting" => Ok(Self::Starting),
            "ready" => Ok(Self::Ready),
            "shutting-down" => Ok(Self::ShuttingDown),
            "failed" => Ok(Self::Failed),
            _ => Err("unsupported health state"),
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct StatusSnapshot {
    pub health: HealthState,
    pub active_jobs: usize,
    pub queued_jobs: usize,
    pub records: usize,
    pub completed_jobs: u64,
    pub failed_jobs: u64,
}

impl Default for StatusSnapshot {
    fn default() -> Self {
        Self {
            health: HealthState::Starting,
            active_jobs: 0,
            queued_jobs: 0,
            records: 0,
            completed_jobs: 0,
            failed_jobs: 0,
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum JobFailure {
    InvalidPayload(String),
    ResultTooLarge,
    Cancelled,
}

pub async fn execute(
    request: &JobRequest,
    max_result_bytes: usize,
    max_sleep: Duration,
) -> Result<JobResult, JobFailure> {
    let value = match request.operation {
        Operation::Uppercase => request.payload.to_uppercase(),
        Operation::WordCount => request.payload.split_whitespace().count().to_string(),
        Operation::Checksum => {
            let hash = request.payload.as_bytes().iter().fold(
                0xcbf2_9ce4_8422_2325_u64,
                |state, byte| (state ^ u64::from(*byte)).wrapping_mul(0x100_0000_01b3),
            );
            format!("{hash:016x}")
        }
        Operation::SleepMs => {
            let millis: u64 = request.payload.parse().map_err(|_| {
                JobFailure::InvalidPayload("sleep-ms payload must be an unsigned integer".to_owned())
            })?;
            let duration = Duration::from_millis(millis);
            if duration > max_sleep {
                return Err(JobFailure::InvalidPayload(format!(
                    "sleep-ms exceeds maximum of {} ms",
                    max_sleep.as_millis()
                )));
            }
            tokio::time::sleep(duration).await;
            format!("slept-{millis}-ms")
        }
    };

    if value.len() > max_result_bytes {
        return Err(JobFailure::ResultTooLarge);
    }
    Ok(JobResult { value })
}
