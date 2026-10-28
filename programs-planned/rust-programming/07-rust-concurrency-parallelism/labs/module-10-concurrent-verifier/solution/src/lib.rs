#![forbid(unsafe_code)]

use std::collections::{BTreeMap, BTreeSet, VecDeque};
use std::panic::{self, AssertUnwindSafe};
use std::sync::atomic::{AtomicBool, AtomicUsize, Ordering};
use std::sync::mpsc;
use std::sync::{Arc, Condvar, Mutex};
use std::thread;

pub const MAX_ARTIFACTS: usize = 4096;
pub const MAX_TOTAL_BYTES: usize = 8 * 1024 * 1024;
pub const MAX_ID_BYTES: usize = 128;
pub const MAX_WORKERS: usize = 64;
pub const MAX_CAPACITY: usize = 4096;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Behavior {
    Verify,
    Panic,
    Spin(usize),
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Artifact {
    pub id: String,
    pub bytes: Vec<u8>,
    pub expected: u64,
    pub behavior: Behavior,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Verification {
    Matched {
        index: usize,
        id: String,
        digest: u64,
    },
    Mismatched {
        index: usize,
        id: String,
        expected: u64,
        actual: u64,
    },
    Panicked {
        index: usize,
        id: String,
    },
    Cancelled {
        index: usize,
        id: String,
    },
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum FailurePolicy {
    Continue,
    FailFast,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum VerifyError {
    ZeroWorkers,
    TooManyWorkers { count: usize, limit: usize },
    ZeroCapacity,
    CapacityTooLarge { count: usize, limit: usize },
    TooManyArtifacts { count: usize, limit: usize },
    TooManyBytes { count: usize, limit: usize },
    EmptyId { index: usize },
    IdTooLong { index: usize, count: usize, limit: usize },
    DuplicateId(String),
    OutcomeOutOfRange { index: usize, count: usize },
    DuplicateOutcome { index: usize },
    MissingOutcome { index: usize },
    WorkerPanicked { worker: usize },
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)]
pub struct LiveMetrics {
    pub started: usize,
    pub terminal: usize,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Report {
    pub outcomes: Vec<Verification>,
    pub by_status: BTreeMap<&'static str, usize>,
    pub live: LiveMetrics,
}

struct State<T> {
    items: VecDeque<T>,
    closed: bool,
}

struct Queue<T> {
    capacity: usize,
    state: Mutex<State<T>>,
    not_empty: Condvar,
    not_full: Condvar,
}

impl<T> Queue<T> {
    fn new(capacity: usize) -> Self {
        Self {
            capacity,
            state: Mutex::new(State {
                items: VecDeque::new(),
                closed: false,
            }),
            not_empty: Condvar::new(),
            not_full: Condvar::new(),
        }
    }

    fn push(&self, item: T) -> Result<(), T> {
        let mut state = self.state.lock().unwrap_or_else(|poison| poison.into_inner());
        while state.items.len() == self.capacity && !state.closed {
            state = self
                .not_full
                .wait(state)
                .unwrap_or_else(|poison| poison.into_inner());
        }
        if state.closed {
            return Err(item);
        }
        state.items.push_back(item);
        self.not_empty.notify_one();
        Ok(())
    }

    fn pop(&self) -> Option<T> {
        let mut state = self.state.lock().unwrap_or_else(|poison| poison.into_inner());
        while state.items.is_empty() && !state.closed {
            state = self
                .not_empty
                .wait(state)
                .unwrap_or_else(|poison| poison.into_inner());
        }
        let item = state.items.pop_front();
        if item.is_some() {
            self.not_full.notify_one();
        }
        item
    }

    fn close(&self) {
        let mut state = self.state.lock().unwrap_or_else(|poison| poison.into_inner());
        state.closed = true;
        drop(state);
        self.not_empty.notify_all();
        self.not_full.notify_all();
    }
}

struct Metrics {
    started: AtomicUsize,
    terminal: AtomicUsize,
}

impl Metrics {
    fn snapshot(&self) -> LiveMetrics {
        LiveMetrics {
            started: self.started.load(Ordering::Relaxed),
            terminal: self.terminal.load(Ordering::Relaxed),
        }
    }
}

#[must_use]
pub fn fnv1a(bytes: &[u8]) -> u64 {
    bytes.iter().fold(0xcbf2_9ce4_8422_2325, |hash, byte| {
        (hash ^ u64::from(*byte)).wrapping_mul(0x0000_0100_0000_01b3)
    })
}

fn execute(index: usize, artifact: &Artifact, cancelled: &AtomicBool) -> Verification {
    match artifact.behavior {
        Behavior::Panic => panic!("injected verifier panic"),
        Behavior::Spin(steps) => {
            for _ in 0..steps {
                if cancelled.load(Ordering::Relaxed) {
                    return Verification::Cancelled {
                        index,
                        id: artifact.id.clone(),
                    };
                }
                thread::yield_now();
            }
        }
        Behavior::Verify => {}
    }

    let actual = fnv1a(&artifact.bytes);
    if actual == artifact.expected {
        Verification::Matched {
            index,
            id: artifact.id.clone(),
            digest: actual,
        }
    } else {
        Verification::Mismatched {
            index,
            id: artifact.id.clone(),
            expected: artifact.expected,
            actual,
        }
    }
}

pub fn verify(
    artifacts: Vec<Artifact>,
    workers: usize,
    capacity: usize,
    policy: FailurePolicy,
) -> Result<Report, VerifyError> {
    validate_inputs(&artifacts, workers, capacity)?;

    let count = artifacts.len();
    let queue = Arc::new(Queue::new(capacity));
    let cancelled = Arc::new(AtomicBool::new(false));
    let metrics = Arc::new(Metrics {
        started: AtomicUsize::new(0),
        terminal: AtomicUsize::new(0),
    });
    let (result_tx, result_rx) = mpsc::channel();
    let mut handles = Vec::with_capacity(workers);

    for worker in 0..workers {
        let queue = Arc::clone(&queue);
        let cancelled = Arc::clone(&cancelled);
        let metrics = Arc::clone(&metrics);
        let result_tx = result_tx.clone();
        handles.push((
            worker,
            thread::spawn(move || {
                while let Some((index, artifact)) = queue.pop() {
                    let outcome = if cancelled.load(Ordering::Relaxed) {
                        Verification::Cancelled {
                            index,
                            id: artifact.id,
                        }
                    } else {
                        metrics.started.fetch_add(1, Ordering::Relaxed);
                        match panic::catch_unwind(AssertUnwindSafe(|| {
                            execute(index, &artifact, &cancelled)
                        })) {
                            Ok(outcome) => outcome,
                            Err(_) => Verification::Panicked {
                                index,
                                id: artifact.id.clone(),
                            },
                        }
                    };

                    if policy == FailurePolicy::FailFast
                        && matches!(
                            outcome,
                            Verification::Mismatched { .. } | Verification::Panicked { .. }
                        )
                    {
                        cancelled.store(true, Ordering::Relaxed);
                        queue.close();
                    }

                    metrics.terminal.fetch_add(1, Ordering::Relaxed);
                    if result_tx.send(outcome).is_err() {
                        cancelled.store(true, Ordering::Relaxed);
                        queue.close();
                        break;
                    }
                }
            }),
        ));
    }
    drop(result_tx);

    let mut rejected = Vec::new();
    let mut iterator = artifacts.into_iter().enumerate();
    while let Some(item) = iterator.next() {
        match queue.push(item) {
            Ok(()) => {}
            Err(item) => {
                rejected.push(item);
                rejected.extend(iterator);
                break;
            }
        }
    }
    queue.close();

    let mut slots: Vec<Option<Verification>> = (0..count).map(|_| None).collect();
    let mut protocol_error = None;
    for outcome in result_rx {
        let index = outcome_index(&outcome);
        let Some(slot) = slots.get_mut(index) else {
            protocol_error.get_or_insert(VerifyError::OutcomeOutOfRange { index, count });
            continue;
        };
        if slot.is_some() {
            protocol_error.get_or_insert(VerifyError::DuplicateOutcome { index });
        } else {
            *slot = Some(outcome);
        }
    }

    let mut first_worker_panic = None;
    for (worker, handle) in handles {
        if handle.join().is_err() && first_worker_panic.is_none() {
            first_worker_panic = Some(VerifyError::WorkerPanicked { worker });
        }
    }

    if let Some(error) = protocol_error {
        return Err(error);
    }
    if let Some(error) = first_worker_panic {
        return Err(error);
    }

    for (index, artifact) in rejected {
        let slot = &mut slots[index];
        if slot.is_some() {
            return Err(VerifyError::DuplicateOutcome { index });
        }
        *slot = Some(Verification::Cancelled {
            index,
            id: artifact.id,
        });
    }

    let outcomes: Vec<_> = slots
        .into_iter()
        .enumerate()
        .map(|(index, outcome)| outcome.ok_or(VerifyError::MissingOutcome { index }))
        .collect::<Result<_, _>>()?;

    let mut by_status = BTreeMap::new();
    for outcome in &outcomes {
        let key = match outcome {
            Verification::Matched { .. } => "matched",
            Verification::Mismatched { .. } => "mismatched",
            Verification::Panicked { .. } => "panicked",
            Verification::Cancelled { .. } => "cancelled",
        };
        *by_status.entry(key).or_default() += 1;
    }

    Ok(Report {
        outcomes,
        by_status,
        live: metrics.snapshot(),
    })
}

fn validate_inputs(
    artifacts: &[Artifact],
    workers: usize,
    capacity: usize,
) -> Result<(), VerifyError> {
    if workers == 0 {
        return Err(VerifyError::ZeroWorkers);
    }
    if workers > MAX_WORKERS {
        return Err(VerifyError::TooManyWorkers {
            count: workers,
            limit: MAX_WORKERS,
        });
    }
    if capacity == 0 {
        return Err(VerifyError::ZeroCapacity);
    }
    if capacity > MAX_CAPACITY {
        return Err(VerifyError::CapacityTooLarge {
            count: capacity,
            limit: MAX_CAPACITY,
        });
    }
    if artifacts.len() > MAX_ARTIFACTS {
        return Err(VerifyError::TooManyArtifacts {
            count: artifacts.len(),
            limit: MAX_ARTIFACTS,
        });
    }

    let total_bytes = artifacts.iter().try_fold(0_usize, |total, artifact| {
        total.checked_add(artifact.bytes.len())
    });
    let total_bytes = total_bytes.unwrap_or(usize::MAX);
    if total_bytes > MAX_TOTAL_BYTES {
        return Err(VerifyError::TooManyBytes {
            count: total_bytes,
            limit: MAX_TOTAL_BYTES,
        });
    }

    let mut ids = BTreeSet::new();
    for (index, artifact) in artifacts.iter().enumerate() {
        if artifact.id.is_empty() {
            return Err(VerifyError::EmptyId { index });
        }
        if artifact.id.len() > MAX_ID_BYTES {
            return Err(VerifyError::IdTooLong {
                index,
                count: artifact.id.len(),
                limit: MAX_ID_BYTES,
            });
        }
        if !ids.insert(artifact.id.as_str()) {
            return Err(VerifyError::DuplicateId(artifact.id.clone()));
        }
    }
    Ok(())
}

fn outcome_index(outcome: &Verification) -> usize {
    match outcome {
        Verification::Matched { index, .. }
        | Verification::Mismatched { index, .. }
        | Verification::Panicked { index, .. }
        | Verification::Cancelled { index, .. } => *index,
    }
}

#[cfg(test)]
mod tests {
    use super::{
        Artifact, Behavior, FailurePolicy, Verification, VerifyError, fnv1a, verify,
    };

    fn artifact(
        id: &str,
        bytes: &[u8],
        behavior: Behavior,
        matching_digest: bool,
    ) -> Artifact {
        let expected = if matching_digest {
            fnv1a(bytes)
        } else {
            fnv1a(bytes).wrapping_add(1)
        };
        Artifact {
            id: id.to_owned(),
            bytes: bytes.to_vec(),
            expected,
            behavior,
        }
    }

    #[test]
    fn continue_mode_is_deterministic_across_worker_and_queue_counts() {
        let fixture = vec![
            artifact("a", b"one", Behavior::Spin(100), true),
            artifact("b", b"two", Behavior::Verify, false),
            artifact("c", b"three", Behavior::Panic, true),
            artifact("d", b"four", Behavior::Verify, true),
        ];
        let one = verify(fixture.clone(), 1, 1, FailurePolicy::Continue)
            .expect("valid configuration");
        let many = verify(fixture, 4, 2, FailurePolicy::Continue)
            .expect("valid configuration");
        assert_eq!(one.outcomes, many.outcomes);
        assert_eq!(one.by_status, many.by_status);
    }

    #[test]
    fn fail_fast_still_accounts_for_every_artifact_in_source_order() {
        let fixture = vec![
            artifact("a", b"a", Behavior::Panic, true),
            artifact("b", b"b", Behavior::Spin(100_000), true),
            artifact("c", b"c", Behavior::Verify, true),
        ];
        let report = verify(fixture, 2, 1, FailurePolicy::FailFast)
            .expect("valid configuration");
        assert_eq!(report.outcomes.len(), 3);
        for (index, outcome) in report.outcomes.iter().enumerate() {
            assert_eq!(super::outcome_index(outcome), index);
        }
        assert!(report
            .outcomes
            .iter()
            .any(|outcome| matches!(outcome, Verification::Panicked { .. })));
    }

    #[test]
    fn final_summary_not_live_metrics_is_authoritative() {
        let report = verify(
            vec![artifact("a", b"a", Behavior::Verify, true)],
            1,
            1,
            FailurePolicy::Continue,
        )
        .expect("valid configuration");
        assert_eq!(report.by_status.values().sum::<usize>(), report.outcomes.len());
    }

    #[test]
    fn rejects_duplicate_identity_and_invalid_resources() {
        let duplicate = artifact("same", b"a", Behavior::Verify, true);
        assert!(matches!(
            verify(
                vec![duplicate.clone(), duplicate],
                1,
                1,
                FailurePolicy::Continue
            ),
            Err(VerifyError::DuplicateId(_))
        ));
        assert_eq!(
            verify(Vec::new(), 0, 1, FailurePolicy::Continue),
            Err(VerifyError::ZeroWorkers)
        );
        assert_eq!(
            verify(Vec::new(), 1, 0, FailurePolicy::Continue),
            Err(VerifyError::ZeroCapacity)
        );
    }
}
