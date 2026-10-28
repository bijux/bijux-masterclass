use crate::{
    config::Config,
    domain::{execute, HealthState, JobFailure, JobRequest, JobResult, StatusSnapshot},
};
use std::collections::{HashMap, VecDeque};
use tokio::{
    sync::{mpsc, oneshot, watch},
    task::{Id, JoinHandle, JoinSet},
};
use tokio_util::sync::CancellationToken;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum TerminalResult {
    Success(JobResult),
    DomainFailure(String),
    Cancelled,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum SubmitReply {
    Terminal(TerminalResult),
    Busy { retry_after_ms: u64 },
    Conflict,
    TooManyWaiters,
    ShuttingDown,
}

#[derive(Debug)]
enum Command {
    Submit {
        request: JobRequest,
        reply: oneshot::Sender<SubmitReply>,
    },
}

#[derive(Debug)]
enum RecordState {
    InProgress {
        waiters: Vec<oneshot::Sender<SubmitReply>>,
    },
    Completed(TerminalResult),
}

#[derive(Debug)]
struct Record {
    fingerprint: String,
    state: RecordState,
}

#[derive(Debug)]
struct PendingJob {
    key: String,
    request: JobRequest,
}

#[derive(Debug)]
struct FinishedJob {
    key: String,
    result: TerminalResult,
}

#[derive(Clone)]
pub struct BrokerHandle {
    tx: mpsc::Sender<Command>,
    status: watch::Receiver<StatusSnapshot>,
}

impl BrokerHandle {
    pub async fn submit(&self, request: JobRequest) -> SubmitReply {
        let (reply_tx, reply_rx) = oneshot::channel();
        if self.tx.send(Command::Submit { request, reply: reply_tx }).await.is_err() {
            return SubmitReply::ShuttingDown;
        }
        reply_rx.await.unwrap_or(SubmitReply::ShuttingDown)
    }

    pub fn snapshot(&self) -> StatusSnapshot {
        self.status.borrow().clone()
    }

    pub fn subscribe(&self) -> watch::Receiver<StatusSnapshot> {
        self.status.clone()
    }
}

pub fn start_broker(
    config: Config,
    cancellation: CancellationToken,
) -> (BrokerHandle, JoinHandle<()>) {
    let (tx, rx) = mpsc::channel(config.broker_capacity);
    let (status_tx, status_rx) = watch::channel(StatusSnapshot::default());
    let handle = BrokerHandle { tx, status: status_rx };
    let task = tokio::spawn(run_broker(config, cancellation, rx, status_tx));
    (handle, task)
}

async fn run_broker(
    config: Config,
    cancellation: CancellationToken,
    mut rx: mpsc::Receiver<Command>,
    status_tx: watch::Sender<StatusSnapshot>,
) {
    let jobs_cancel = cancellation.child_token();
    let mut records: HashMap<String, Record> = HashMap::new();
    let mut record_order = VecDeque::new();
    let mut pending = VecDeque::new();
    let mut active = JoinSet::new();
    let mut active_keys: HashMap<Id, String> = HashMap::new();
    let mut completed_jobs = 0_u64;
    let mut failed_jobs = 0_u64;
    let mut shutting_down = false;

    publish(
        &status_tx,
        HealthState::Ready,
        active.len(),
        pending.len(),
        records.len(),
        completed_jobs,
        failed_jobs,
    );

    loop {
        while !shutting_down && active.len() < config.max_active_jobs {
            let Some(job) = pending.pop_front() else {
                break;
            };
            spawn_job(
                &mut active,
                &mut active_keys,
                job,
                &config,
                jobs_cancel.child_token(),
            );
        }

        publish(
            &status_tx,
            if shutting_down { HealthState::ShuttingDown } else { HealthState::Ready },
            active.len(),
            pending.len(),
            records.len(),
            completed_jobs,
            failed_jobs,
        );

        if shutting_down && active.is_empty() && pending.is_empty() {
            break;
        }

        tokio::select! {
            () = cancellation.cancelled(), if !shutting_down => {
                shutting_down = true;
                rx.close();
                reject_buffered(&mut rx);
                jobs_cancel.cancel();
                reject_pending(&mut pending, &mut records);
            }
            command = rx.recv(), if !shutting_down => {
                match command {
                    Some(Command::Submit { request, reply }) => {
                        accept_submit(
                            request,
                            reply,
                            &config,
                            &mut records,
                            &mut record_order,
                            &mut pending,
                            &mut active,
                            &mut active_keys,
                            jobs_cancel.child_token(),
                        );
                    }
                    None => {
                        shutting_down = true;
                        jobs_cancel.cancel();
                        reject_pending(&mut pending, &mut records);
                    }
                }
            }
            joined = active.join_next_with_id(), if !active.is_empty() => {
                match joined {
                    Some(Ok((id, finished))) => {
                        debug_assert!(active_keys.remove(&id).is_some());
                        match &finished.result {
                            TerminalResult::Success(_) => completed_jobs += 1,
                            TerminalResult::DomainFailure(_) | TerminalResult::Cancelled => failed_jobs += 1,
                        }
                        complete_record(finished, &mut records);
                    }
                    Some(Err(join_error)) => {
                        failed_jobs += 1;
                        if let Some(key) = active_keys.remove(&join_error.id()) {
                            let result = if join_error.is_cancelled() {
                                TerminalResult::Cancelled
                            } else {
                                TerminalResult::DomainFailure("job task panicked".to_owned())
                            };
                            complete_record(FinishedJob { key, result }, &mut records);
                        }
                    }
                    None => {}
                }
            }
        }
    }

    active.abort_all();
    while let Some(joined) = active.join_next_with_id().await {
        match joined {
            Ok((id, finished)) => {
                debug_assert!(active_keys.remove(&id).is_some());
                complete_record(finished, &mut records);
            }
            Err(error) => {
                if let Some(key) = active_keys.remove(&error.id()) {
                    complete_record(
                        FinishedJob { key, result: TerminalResult::Cancelled },
                        &mut records,
                    );
                }
            }
        }
    }
    publish(
        &status_tx,
        HealthState::ShuttingDown,
        0,
        0,
        records.len(),
        completed_jobs,
        failed_jobs,
    );
}

#[allow(clippy::too_many_arguments)]
fn accept_submit(
    request: JobRequest,
    reply: oneshot::Sender<SubmitReply>,
    config: &Config,
    records: &mut HashMap<String, Record>,
    record_order: &mut VecDeque<String>,
    pending: &mut VecDeque<PendingJob>,
    active: &mut JoinSet<FinishedJob>,
    active_keys: &mut HashMap<Id, String>,
    cancellation: CancellationToken,
) {
    let key = request.idempotency_key.clone();
    let fingerprint = request.fingerprint();

    if let Some(record) = records.get_mut(&key) {
        if record.fingerprint != fingerprint {
            let _ = reply.send(SubmitReply::Conflict);
            return;
        }
        match &mut record.state {
            RecordState::Completed(result) => {
                let _ = reply.send(SubmitReply::Terminal(result.clone()));
            }
            RecordState::InProgress { waiters } => {
                if waiters.len() >= config.max_waiters_per_key {
                    let _ = reply.send(SubmitReply::TooManyWaiters);
                } else {
                    waiters.push(reply);
                }
            }
        }
        return;
    }

    let can_start = active.len() < config.max_active_jobs;
    if !can_start && pending.len() >= config.max_queued_jobs {
        let _ = reply.send(SubmitReply::Busy { retry_after_ms: 100 });
        return;
    }

    if records.len() >= config.max_idempotency_records
        && !evict_one_completed(records, record_order)
    {
        let _ = reply.send(SubmitReply::Busy { retry_after_ms: 250 });
        return;
    }

    let previous = records.insert(
        key.clone(),
        Record {
            fingerprint,
            state: RecordState::InProgress { waiters: vec![reply] },
        },
    );
    debug_assert!(previous.is_none());
    record_order.push_back(key.clone());
    let job = PendingJob { key, request };
    if can_start {
        spawn_job(active, active_keys, job, config, cancellation);
    } else {
        pending.push_back(job);
    }
}

fn spawn_job(
    active: &mut JoinSet<FinishedJob>,
    active_keys: &mut HashMap<Id, String>,
    job: PendingJob,
    config: &Config,
    cancellation: CancellationToken,
) {
    let max_result_bytes = config.max_result_bytes;
    let max_sleep = config.max_sleep;
    let key = job.key.clone();
    let abort_handle = active.spawn(async move {
        let result = tokio::select! {
            () = cancellation.cancelled() => TerminalResult::Cancelled,
            outcome = execute(&job.request, max_result_bytes, max_sleep) => match outcome {
                Ok(value) => TerminalResult::Success(value),
                Err(error) => TerminalResult::DomainFailure(render_failure(error)),
            }
        };
        FinishedJob { key: job.key, result }
    });
    debug_assert!(active_keys.insert(abort_handle.id(), key).is_none());
}

fn render_failure(error: JobFailure) -> String {
    match error {
        JobFailure::InvalidPayload(message) => message,
        JobFailure::ResultTooLarge => "result exceeds configured maximum".to_owned(),
        JobFailure::Cancelled => "job cancelled".to_owned(),
    }
}

fn complete_record(finished: FinishedJob, records: &mut HashMap<String, Record>) {
    let Some(record) = records.get_mut(&finished.key) else {
        return;
    };
    let waiters = match std::mem::replace(
        &mut record.state,
        RecordState::Completed(finished.result.clone()),
    ) {
        RecordState::InProgress { waiters } => waiters,
        RecordState::Completed(previous) => {
            record.state = RecordState::Completed(previous);
            return;
        }
    };
    for waiter in waiters {
        let _ = waiter.send(SubmitReply::Terminal(finished.result.clone()));
    }
}

fn reject_pending(
    pending: &mut VecDeque<PendingJob>,
    records: &mut HashMap<String, Record>,
) {
    while let Some(job) = pending.pop_front() {
        complete_record(
            FinishedJob {
                key: job.key,
                result: TerminalResult::Cancelled,
            },
            records,
        );
    }
}

fn reject_buffered(rx: &mut mpsc::Receiver<Command>) {
    while let Ok(command) = rx.try_recv() {
        match command {
            Command::Submit { reply, .. } => {
                let _ = reply.send(SubmitReply::ShuttingDown);
            }
        }
    }
}

fn evict_one_completed(
    records: &mut HashMap<String, Record>,
    order: &mut VecDeque<String>,
) -> bool {
    let attempts = order.len();
    for _ in 0..attempts {
        let Some(key) = order.pop_front() else {
            return false;
        };
        let completed = records
            .get(&key)
            .is_some_and(|record| matches!(record.state, RecordState::Completed(_)));
        if completed {
            debug_assert!(records.remove(&key).is_some());
            return true;
        }
        order.push_back(key);
    }
    false
}

fn publish(
    tx: &watch::Sender<StatusSnapshot>,
    health: HealthState,
    active_jobs: usize,
    queued_jobs: usize,
    records: usize,
    completed_jobs: u64,
    failed_jobs: u64,
) {
    let _previous = tx.send_replace(StatusSnapshot {
        health,
        active_jobs,
        queued_jobs,
        records,
        completed_jobs,
        failed_jobs,
    });
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::domain::Operation;

    fn request(key: &str, payload: &str) -> JobRequest {
        JobRequest {
            idempotency_key: key.to_owned(),
            operation: Operation::Uppercase,
            payload: payload.to_owned(),
        }
    }

    #[tokio::test]
    async fn duplicate_key_returns_one_result() {
        let cancellation = CancellationToken::new();
        let (broker, task) = start_broker(Config::default(), cancellation.clone());
        let first = broker.submit(request("key", "hello")).await;
        let second = broker.submit(request("key", "hello")).await;
        assert_eq!(first, second);
        cancellation.cancel();
        task.await.unwrap();
    }

    #[tokio::test]
    async fn changed_payload_conflicts() {
        let cancellation = CancellationToken::new();
        let (broker, task) = start_broker(Config::default(), cancellation.clone());
        let _ = broker.submit(request("key", "hello")).await;
        assert_eq!(broker.submit(request("key", "changed")).await, SubmitReply::Conflict);
        cancellation.cancel();
        task.await.unwrap();
    }
}
