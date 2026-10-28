//! Idempotent retry under ambiguous commit.
//!
//! The client retry loop and the server idempotency store solve different
//! problems. The loop controls attempts, delay, and deadline. The store gives
//! several wire attempts one semantic identity and caches both successful and
//! terminal domain outcomes.

use std::{collections::{HashMap, VecDeque}, future::Future, time::Duration};

use tokio::time::{self, Instant};

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct RetryPolicy {
    pub max_attempts: u32,
    pub initial_delay: Duration,
    pub max_delay: Duration,
    pub overall_deadline: Duration,
}

impl RetryPolicy {
    pub fn validate(self) -> Result<Self, PolicyError> {
        if self.max_attempts == 0 {
            return Err(PolicyError::ZeroAttempts);
        }
        if self.initial_delay.is_zero() || self.max_delay.is_zero() {
            return Err(PolicyError::ZeroDelay);
        }
        if self.initial_delay > self.max_delay {
            return Err(PolicyError::InvertedDelayRange);
        }
        if self.overall_deadline.is_zero() {
            return Err(PolicyError::ZeroDeadline);
        }
        Ok(self)
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum PolicyError {
    ZeroAttempts,
    ZeroDelay,
    InvertedDelayRange,
    ZeroDeadline,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Failure {
    Busy { retry_after: Option<Duration> },
    Transport,
    Conflict,
    Capacity,
    Domain(String),
}

impl Failure {
    pub fn is_retryable(&self) -> bool {
        matches!(self, Self::Busy { .. } | Self::Transport)
    }

    fn retry_hint(&self) -> Option<Duration> {
        match self {
            Self::Busy { retry_after } => *retry_after,
            _ => None,
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum RetryError {
    InvalidPolicy(PolicyError),
    Terminal(Failure),
    AttemptsExhausted { last: Failure },
    Deadline { last: Option<Failure> },
}

#[derive(Debug, Clone, PartialEq, Eq)]
enum StoredOutcome {
    Success(String),
    DomainFailure(String),
}

#[derive(Debug, Clone, PartialEq, Eq)]
enum RecordState {
    InProgress,
    Completed(StoredOutcome),
}

#[derive(Debug, Clone, PartialEq, Eq)]
struct Record {
    fingerprint: String,
    state: RecordState,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Begin {
    Execute,
    Cached(Result<String, String>),
    InProgress,
    Conflict,
    Capacity,
}

#[derive(Debug)]
pub struct IdempotencyStore {
    record_limit: usize,
    records: HashMap<String, Record>,
    semantic_executions: usize,
}

impl IdempotencyStore {
    pub fn new(record_limit: usize) -> Result<Self, &'static str> {
        if record_limit == 0 {
            return Err("record_limit must be nonzero");
        }
        Ok(Self {
            record_limit,
            records: HashMap::new(),
            semantic_executions: 0,
        })
    }

    pub fn begin(&mut self, key: &str, fingerprint: &str) -> Begin {
        if let Some(record) = self.records.get(key) {
            if record.fingerprint != fingerprint {
                return Begin::Conflict;
            }
            return match &record.state {
                RecordState::InProgress => Begin::InProgress,
                RecordState::Completed(StoredOutcome::Success(value)) => {
                    Begin::Cached(Ok(value.clone()))
                }
                RecordState::Completed(StoredOutcome::DomainFailure(message)) => {
                    Begin::Cached(Err(message.clone()))
                }
            };
        }

        if self.records.len() >= self.record_limit {
            return Begin::Capacity;
        }

        let previous = self.records.insert(
            key.to_owned(),
            Record {
                fingerprint: fingerprint.to_owned(),
                state: RecordState::InProgress,
            },
        );
        debug_assert!(previous.is_none());
        self.semantic_executions += 1;
        Begin::Execute
    }

    pub fn complete_success(&mut self, key: &str, value: String) -> Result<(), &'static str> {
        self.complete(key, StoredOutcome::Success(value))
    }

    pub fn complete_domain_failure(
        &mut self,
        key: &str,
        message: String,
    ) -> Result<(), &'static str> {
        self.complete(key, StoredOutcome::DomainFailure(message))
    }

    fn complete(&mut self, key: &str, outcome: StoredOutcome) -> Result<(), &'static str> {
        let record = self
            .records
            .get_mut(key)
            .ok_or("cannot complete an unknown key")?;
        if record.state != RecordState::InProgress {
            return Err("a completed key cannot be completed again");
        }
        record.state = RecordState::Completed(outcome);
        Ok(())
    }

    pub fn execution_count(&self) -> usize {
        self.semantic_executions
    }

    pub fn record_count(&self) -> usize {
        self.records.len()
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ScriptStep {
    Busy { retry_after: Option<Duration> },
    TransportBeforeCommit,
    DisconnectAfterCommit,
    Deliver,
    DomainFailure(String),
}

#[derive(Debug)]
pub struct ScriptedServer {
    store: IdempotencyStore,
    script: VecDeque<ScriptStep>,
    wire_attempts: usize,
}

impl ScriptedServer {
    pub fn new(record_limit: usize, script: impl IntoIterator<Item = ScriptStep>) -> Self {
        Self {
            store: IdempotencyStore::new(record_limit)
                .expect("test server record limit must be nonzero"),
            script: script.into_iter().collect(),
            wire_attempts: 0,
        }
    }

    pub fn attempt(
        &mut self,
        key: &str,
        fingerprint: &str,
        payload: &str,
    ) -> Result<String, Failure> {
        self.wire_attempts += 1;
        let step = self.script.pop_front().unwrap_or(ScriptStep::Deliver);

        match step {
            ScriptStep::Busy { retry_after } => {
                return Err(Failure::Busy { retry_after });
            }
            ScriptStep::TransportBeforeCommit => return Err(Failure::Transport),
            _ => {}
        }

        match self.store.begin(key, fingerprint) {
            Begin::Conflict => return Err(Failure::Conflict),
            Begin::Capacity => return Err(Failure::Capacity),
            Begin::InProgress => {
                return Err(Failure::Busy {
                    retry_after: Some(Duration::from_millis(25)),
                });
            }
            Begin::Cached(Ok(value)) => return Ok(value),
            Begin::Cached(Err(message)) => return Err(Failure::Domain(message)),
            Begin::Execute => {}
        }

        match step {
            ScriptStep::DisconnectAfterCommit => {
                let value = execute(payload);
                self.store
                    .complete_success(key, value)
                    .expect("a newly executing key must be completable");
                Err(Failure::Transport)
            }
            ScriptStep::Deliver => {
                let value = execute(payload);
                self.store
                    .complete_success(key, value.clone())
                    .expect("a newly executing key must be completable");
                Ok(value)
            }
            ScriptStep::DomainFailure(message) => {
                self.store
                    .complete_domain_failure(key, message.clone())
                    .expect("a newly executing key must be completable");
                Err(Failure::Domain(message))
            }
            ScriptStep::Busy { .. } | ScriptStep::TransportBeforeCommit => {
                unreachable!("pre-commit script steps returned before store admission")
            }
        }
    }

    pub fn execution_count(&self) -> usize {
        self.store.execution_count()
    }

    pub fn attempt_count(&self) -> usize {
        self.wire_attempts
    }
}

fn execute(payload: &str) -> String {
    payload.trim().to_uppercase()
}

pub async fn retry<T, F, Fut, J>(
    policy: RetryPolicy,
    mut attempt: F,
    mut jitter: J,
) -> Result<T, RetryError>
where
    F: FnMut(u32) -> Fut,
    Fut: Future<Output = Result<T, Failure>>,
    J: FnMut(Duration, u32) -> Duration,
{
    let policy = policy.validate().map_err(RetryError::InvalidPolicy)?;
    let deadline = Instant::now() + policy.overall_deadline;
    let mut base_delay = policy.initial_delay;
    let mut last_failure: Option<Failure> = None;

    for attempt_number in 1..=policy.max_attempts {
        let result = match time::timeout_at(deadline, attempt(attempt_number)).await {
            Ok(result) => result,
            Err(_) => {
                return Err(RetryError::Deadline {
                    last: last_failure,
                });
            }
        };

        match result {
            Ok(value) => return Ok(value),
            Err(failure) if !failure.is_retryable() => {
                return Err(RetryError::Terminal(failure));
            }
            Err(failure) if attempt_number == policy.max_attempts => {
                return Err(RetryError::AttemptsExhausted { last: failure });
            }
            Err(failure) => {
                let requested = failure
                    .retry_hint()
                    .map_or(base_delay, |hint| hint.max(base_delay))
                    .min(policy.max_delay);
                let delay = jitter(requested, attempt_number).min(policy.max_delay);
                last_failure = Some(failure);

                let Some(wakeup) = Instant::now().checked_add(delay) else {
                    return Err(RetryError::Deadline {
                        last: last_failure,
                    });
                };
                if wakeup >= deadline {
                    return Err(RetryError::Deadline {
                        last: last_failure,
                    });
                }

                time::sleep_until(wakeup).await;
                base_delay = base_delay.saturating_mul(2).min(policy.max_delay);
            }
        }
    }

    unreachable!("validated policy always executes at least one attempt")
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::sync::Arc;
    use tokio::{sync::Mutex, task};

    fn policy() -> RetryPolicy {
        RetryPolicy {
            max_attempts: 4,
            initial_delay: Duration::from_secs(1),
            max_delay: Duration::from_secs(4),
            overall_deadline: Duration::from_secs(20),
        }
    }

    #[tokio::test(start_paused = true)]
    async fn commit_then_disconnect_reuses_one_semantic_execution() {
        let server = Arc::new(Mutex::new(ScriptedServer::new(
            8,
            [ScriptStep::DisconnectAfterCommit, ScriptStep::Deliver],
        )));
        let task_server = Arc::clone(&server);

        let operation = task::spawn(async move {
            retry(
                policy(),
                move |_| {
                    let server = Arc::clone(&task_server);
                    async move { server.lock().await.attempt("key-1", "fp-1", " hello ") }
                },
                |delay, _| delay,
            )
            .await
        });

        task::yield_now().await;
        time::advance(Duration::from_secs(1)).await;
        assert_eq!(operation.await.unwrap().unwrap(), "HELLO");

        let server = server.lock().await;
        assert_eq!(server.attempt_count(), 2);
        assert_eq!(server.execution_count(), 1);
    }

    #[tokio::test(start_paused = true)]
    async fn retry_after_hint_is_honored_under_virtual_time() {
        let server = Arc::new(Mutex::new(ScriptedServer::new(
            8,
            [
                ScriptStep::Busy {
                    retry_after: Some(Duration::from_secs(3)),
                },
                ScriptStep::Deliver,
            ],
        )));
        let task_server = Arc::clone(&server);

        let operation = task::spawn(async move {
            retry(
                policy(),
                move |_| {
                    let server = Arc::clone(&task_server);
                    async move { server.lock().await.attempt("key-2", "fp-2", "value") }
                },
                |delay, _| delay,
            )
            .await
        });

        task::yield_now().await;
        time::advance(Duration::from_secs(2)).await;
        assert!(!operation.is_finished());
        time::advance(Duration::from_secs(1)).await;
        assert_eq!(operation.await.unwrap().unwrap(), "VALUE");
    }

    #[tokio::test(start_paused = true)]
    async fn changed_fingerprint_is_terminal_and_not_retried() {
        let server = Arc::new(Mutex::new(ScriptedServer::new(8, [ScriptStep::Deliver])));
        {
            let mut server = server.lock().await;
            assert_eq!(
                server.attempt("same-key", "first", "payload"),
                Ok("PAYLOAD".to_owned())
            );
        }

        let task_server = Arc::clone(&server);
        let result = retry(
            policy(),
            move |_| {
                let server = Arc::clone(&task_server);
                async move {
                    server
                        .lock()
                        .await
                        .attempt("same-key", "changed", "payload")
                }
            },
            |delay, _| delay,
        )
        .await;

        assert_eq!(result, Err(RetryError::Terminal(Failure::Conflict)));
        assert_eq!(server.lock().await.execution_count(), 1);
    }

    #[tokio::test(start_paused = true)]
    async fn terminal_domain_failure_is_cached() {
        let mut server = ScriptedServer::new(
            8,
            [
                ScriptStep::DomainFailure("rejected".to_owned()),
                ScriptStep::Deliver,
            ],
        );

        assert_eq!(
            server.attempt("key", "fp", "payload"),
            Err(Failure::Domain("rejected".to_owned()))
        );
        assert_eq!(
            server.attempt("key", "fp", "payload"),
            Err(Failure::Domain("rejected".to_owned()))
        );
        assert_eq!(server.execution_count(), 1);
    }

    #[tokio::test(start_paused = true)]
    async fn deadline_can_end_retry_before_the_next_delay() {
        let short = RetryPolicy {
            max_attempts: 5,
            initial_delay: Duration::from_secs(1),
            max_delay: Duration::from_secs(10),
            overall_deadline: Duration::from_secs(5),
        };

        let result = retry::<(), _, _, _>(
            short,
            |_| async {
                Err(Failure::Busy {
                    retry_after: Some(Duration::from_secs(10)),
                })
            },
            |delay, _| delay,
        )
        .await;

        assert!(matches!(result, Err(RetryError::Deadline { .. })));
    }

    #[test]
    fn idempotency_store_is_bounded() {
        let mut store = IdempotencyStore::new(1).unwrap();
        assert_eq!(store.begin("one", "fp"), Begin::Execute);
        assert_eq!(store.begin("two", "fp"), Begin::Capacity);
        assert_eq!(store.record_count(), 1);
    }
}
