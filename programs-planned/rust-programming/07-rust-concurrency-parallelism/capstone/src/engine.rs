use crate::domain::{
    EngineConfig, FailurePolicy, Job, JobOutcome, OutcomeKind, RunReport,
};
use crate::error::RunError;
use crate::metrics::Metrics;
use crate::operations;
use crate::queue::{BoundedQueue, Closed};
use crate::report::summarize_parallel;
use std::collections::BTreeSet;
use std::panic::{self, AssertUnwindSafe};
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::mpsc;
use std::sync::Arc;
use std::thread;

pub fn run_jobs(jobs: Vec<Job>, config: EngineConfig) -> Result<RunReport, RunError> {
    validate_jobs(&jobs)?;

    let job_count = jobs.len();
    let queue = Arc::new(BoundedQueue::new(config.queue_capacity));
    let cancelled = Arc::new(AtomicBool::new(false));
    let metrics = Arc::new(Metrics::default());
    let (result_tx, result_rx) = mpsc::channel::<JobOutcome>();
    let mut handles = Vec::with_capacity(config.workers.get());

    for worker in 0..config.workers.get() {
        let queue = Arc::clone(&queue);
        let cancelled = Arc::clone(&cancelled);
        let metrics = Arc::clone(&metrics);
        let result_tx = result_tx.clone();
        let name = format!("batchweave-worker-{worker}");
        match thread::Builder::new().name(name).spawn(move || {
            worker_loop(
                queue,
                cancelled,
                metrics,
                result_tx,
                config.failure_policy,
            );
        }) {
            Ok(handle) => handles.push((worker, handle)),
            Err(error) => {
                queue.close();
                drop(result_tx);
                for (_, handle) in handles {
                    let _ = handle.join();
                }
                return Err(RunError::ThreadSpawn {
                    worker,
                    message: error.to_string(),
                });
            }
        }
    }
    drop(result_tx);

    let mut rejected = Vec::new();
    let mut iterator = jobs.into_iter();
    while let Some(job) = iterator.next() {
        match queue.push(job) {
            Ok(()) => metrics.submitted(),
            Err(Closed(job)) => {
                rejected.push(job);
                rejected.extend(iterator);
                break;
            }
        }
    }
    queue.close();

    let mut slots: Vec<Option<JobOutcome>> = (0..job_count).map(|_| None).collect();
    let mut protocol_error = None;
    for outcome in result_rx {
        let index = outcome.index;
        let Some(slot) = slots.get_mut(index) else {
            protocol_error.get_or_insert(RunError::OutcomeOutOfRange {
                index,
                count: job_count,
            });
            continue;
        };
        if slot.is_some() {
            protocol_error.get_or_insert(RunError::DuplicateOutcome { index });
        } else {
            *slot = Some(outcome);
        }
    }

    let mut first_worker_panic = None;
    for (worker, handle) in handles {
        if handle.join().is_err() && first_worker_panic.is_none() {
            first_worker_panic = Some(RunError::WorkerPanicked { worker });
        }
    }

    if let Some(error) = protocol_error {
        return Err(error);
    }
    if let Some(error) = first_worker_panic {
        return Err(error);
    }

    for job in rejected {
        let index = job.index;
        if let Some(slot) = slots.get_mut(index) {
            if slot.is_none() {
                metrics.cancelled();
                *slot = Some(JobOutcome {
                    index,
                    id: job.id,
                    operation: job.operation,
                    kind: OutcomeKind::Cancelled,
                });
            }
        }
    }

    let mut outcomes = Vec::with_capacity(job_count);
    for (index, slot) in slots.into_iter().enumerate() {
        let Some(outcome) = slot else {
            return Err(RunError::MissingOutcome { index });
        };
        outcomes.push(outcome);
    }

    let summary = summarize_parallel(&outcomes, config.report_threads)?;
    Ok(RunReport {
        outcomes,
        summary,
        live_metrics_at_end: metrics.snapshot(),
    })
}

fn worker_loop(
    queue: Arc<BoundedQueue<Job>>,
    cancelled: Arc<AtomicBool>,
    metrics: Arc<Metrics>,
    result_tx: mpsc::Sender<JobOutcome>,
    failure_policy: FailurePolicy,
) {
    while let Some(job) = queue.pop() {
        let outcome = if cancelled.load(Ordering::Relaxed) {
            metrics.cancelled();
            cancelled_outcome(job)
        } else {
            metrics.started();
            let result = panic::catch_unwind(AssertUnwindSafe(|| operations::execute(&job)));
            match result {
                Ok(Ok(value)) => {
                    metrics.completed();
                    JobOutcome {
                        index: job.index,
                        id: job.id,
                        operation: job.operation,
                        kind: OutcomeKind::Completed(value),
                    }
                }
                Ok(Err(error)) => {
                    metrics.failed();
                    if failure_policy == FailurePolicy::FailFast {
                        cancelled.store(true, Ordering::Relaxed);
                        queue.close();
                    }
                    JobOutcome {
                        index: job.index,
                        id: job.id,
                        operation: job.operation,
                        kind: OutcomeKind::DomainFailed(error.to_string()),
                    }
                }
                Err(_) => {
                    metrics.panicked();
                    cancelled.store(true, Ordering::Relaxed);
                    queue.close();
                    JobOutcome {
                        index: job.index,
                        id: job.id,
                        operation: job.operation,
                        kind: OutcomeKind::Panicked,
                    }
                }
            }
        };

        if result_tx.send(outcome).is_err() {
            cancelled.store(true, Ordering::Relaxed);
            queue.close();
            break;
        }
    }
}

fn cancelled_outcome(job: Job) -> JobOutcome {
    JobOutcome {
        index: job.index,
        id: job.id,
        operation: job.operation,
        kind: OutcomeKind::Cancelled,
    }
}

fn validate_jobs(jobs: &[Job]) -> Result<(), RunError> {
    let mut ids = BTreeSet::new();
    for (position, job) in jobs.iter().enumerate() {
        if job.index != position {
            return Err(RunError::InvalidJobIndex {
                position,
                observed: job.index,
            });
        }
        if !ids.insert(job.id.as_str()) {
            return Err(RunError::DuplicateJobId(job.id.to_string()));
        }
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::run_jobs;
    use crate::domain::{EngineConfig, FailurePolicy, Job, JobId, Operation, OutcomeKind};

    fn job(index: usize, operation: Operation, payload: &str) -> Job {
        Job {
            index,
            id: JobId::new(format!("job-{index}")).expect("valid id"),
            operation,
            payload: payload.to_owned(),
        }
    }

    #[test]
    fn output_is_deterministic_across_worker_and_queue_counts() {
        let jobs = vec![
            job(0, Operation::PrimeCount, "20000"),
            job(1, Operation::WordCount, "one two three"),
            job(2, Operation::SortIntegers, "9,1,5"),
            job(3, Operation::Checksum, "abc"),
        ];
        let a = run_jobs(
            jobs.clone(),
            EngineConfig::new(1, 1, 1, FailurePolicy::Continue).expect("config"),
        )
        .expect("run");
        let b = run_jobs(
            jobs,
            EngineConfig::new(4, 2, 3, FailurePolicy::Continue).expect("config"),
        )
        .expect("run");
        assert_eq!(a.outcomes, b.outcomes);
        assert_eq!(a.summary, b.summary);
    }

    #[test]
    fn domain_failure_continues_when_configured() {
        let report = run_jobs(
            vec![
                job(0, Operation::SortIntegers, "1,nope"),
                job(1, Operation::WordCount, "still runs"),
            ],
            EngineConfig::new(2, 1, 1, FailurePolicy::Continue).expect("config"),
        )
        .expect("run");
        assert!(matches!(&report.outcomes[0].kind, OutcomeKind::DomainFailed(_)));
        assert!(matches!(&report.outcomes[1].kind, OutcomeKind::Completed(_)));
    }

    #[test]
    fn panic_cancels_but_preserves_one_outcome_per_job() {
        let report = run_jobs(
            vec![
                job(0, Operation::Panic, ""),
                job(1, Operation::PrimeCount, "200000"),
                job(2, Operation::Checksum, "later"),
            ],
            EngineConfig::new(2, 1, 1, FailurePolicy::Continue).expect("config"),
        )
        .expect("run");
        assert_eq!(report.outcomes.len(), 3);
        assert!(matches!(&report.outcomes[0].kind, OutcomeKind::Panicked));
        assert_eq!(report.summary.total, 3);
    }
}
