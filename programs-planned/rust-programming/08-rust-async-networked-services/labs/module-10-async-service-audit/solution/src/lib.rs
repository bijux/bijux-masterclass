//! A bounded in-memory notification service used for final Course 8 transfer.
//!
//! One dispatcher owns the committed queue, idempotency records, active task
//! set, and terminal outcomes. Callers own only pre-admission commands and
//! reply receivers. This makes the authority, commitment point, and shutdown
//! proof visible in one place.

use std::{
    collections::{BTreeMap, HashMap, VecDeque},
    time::Duration,
};

use tokio::{
    sync::{mpsc, oneshot, watch},
    task::{Id, JoinHandle, JoinSet},
    time,
};
use tokio_util::sync::CancellationToken;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Limits {
    pub mailbox: usize,
    pub pending: usize,
    pub active: usize,
    pub records: usize,
    pub waiters_per_key: usize,
    pub shutdown_grace: Duration,
}

impl Limits {
    pub fn validate(self) -> Result<Self, ConfigError> {
        if !(1..=16).contains(&self.mailbox) {
            return Err(ConfigError::Mailbox);
        }
        if !(1..=16).contains(&self.pending) {
            return Err(ConfigError::Pending);
        }
        if !(1..=4).contains(&self.active) {
            return Err(ConfigError::Active);
        }
        if !(1..=64).contains(&self.records) {
            return Err(ConfigError::Records);
        }
        if !(1..=8).contains(&self.waiters_per_key) {
            return Err(ConfigError::WaitersPerKey);
        }
        if self.shutdown_grace.is_zero() {
            return Err(ConfigError::ShutdownGrace);
        }
        Ok(self)
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ConfigError {
    Mailbox,
    Pending,
    Active,
    Records,
    WaitersPerKey,
    ShutdownGrace,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Reply {
    Delivered,
    Failed(String),
    Panicked,
    Conflict,
    Busy,
    Cancelled,
    ShuttingDown,
    Invalid(String),
}

#[derive(Debug, Clone, PartialEq, Eq, Default)]
pub struct Snapshot {
    pub accepting: bool,
    pub pending: usize,
    pub active: usize,
    pub records: usize,
    pub terminal: usize,
}

#[derive(Debug, Clone, PartialEq, Eq, Default)]
pub struct Report {
    pub outcomes: BTreeMap<String, Reply>,
    pub committed: usize,
    pub executions: usize,
}

impl Report {
    pub fn terminal_count(&self) -> usize {
        self.outcomes.len()
    }
}

struct Submit {
    key: String,
    recipient: String,
    reply: oneshot::Sender<Reply>,
}

struct Pending {
    key: String,
    recipient: String,
}

struct Record {
    recipient: String,
    state: RecordState,
}

enum RecordState {
    InProgress {
        waiters: Vec<oneshot::Sender<Reply>>,
    },
    Completed(Reply),
}

#[derive(Debug, Clone, PartialEq, Eq)]
enum DeliveryExit {
    Delivered,
    Failed(String),
    Cancelled,
}

#[derive(Clone)]
pub struct Service {
    submissions: mpsc::Sender<Submit>,
    shutdown_request: CancellationToken,
    snapshot: watch::Receiver<Snapshot>,
}

impl Service {
    pub async fn submit(&self, key: &str, recipient: &str) -> Reply {
        if let Err(message) = validate_submission(key, recipient) {
            return Reply::Invalid(message.to_owned());
        }
        if self.shutdown_request.is_cancelled() {
            return Reply::ShuttingDown;
        }

        let (reply_tx, reply_rx) = oneshot::channel();
        let submit = Submit {
            key: key.to_owned(),
            recipient: recipient.to_owned(),
            reply: reply_tx,
        };

        match self.submissions.try_send(submit) {
            Ok(()) => {}
            Err(mpsc::error::TrySendError::Full(_)) => return Reply::Busy,
            Err(mpsc::error::TrySendError::Closed(_)) => return Reply::ShuttingDown,
        }

        reply_rx.await.unwrap_or(Reply::ShuttingDown)
    }

    pub fn snapshot(&self) -> Snapshot {
        self.snapshot.borrow().clone()
    }

    /// Requests one idempotent shutdown transition.
    pub fn request_shutdown(&self) {
        self.shutdown_request.cancel();
    }
}

pub fn start(limits: Limits) -> Result<(Service, JoinHandle<Report>), ConfigError> {
    let limits = limits.validate()?;
    let (submission_tx, submission_rx) = mpsc::channel(limits.mailbox);
    let shutdown_request = CancellationToken::new();
    let (snapshot_tx, snapshot_rx) = watch::channel(Snapshot {
        accepting: true,
        ..Snapshot::default()
    });

    let task = tokio::spawn(run_dispatcher(
        limits,
        submission_rx,
        shutdown_request.clone(),
        snapshot_tx,
    ));

    Ok((
        Service {
            submissions: submission_tx,
            shutdown_request,
            snapshot: snapshot_rx,
        },
        task,
    ))
}

async fn run_dispatcher(
    limits: Limits,
    mut submissions: mpsc::Receiver<Submit>,
    shutdown_request: CancellationToken,
    snapshot_tx: watch::Sender<Snapshot>,
) -> Report {
    let child_cancel = CancellationToken::new();
    let mut pending = VecDeque::<Pending>::new();
    let mut active = JoinSet::<DeliveryExit>::new();
    let mut active_keys = HashMap::<Id, String>::new();
    let mut records = HashMap::<String, Record>::new();
    let mut report = Report::default();
    let mut accepting = true;

    while accepting {
        start_ready_deliveries(
            limits.active,
            &mut pending,
            &mut active,
            &mut active_keys,
            &child_cancel,
            &mut report,
        );
        publish(
            &snapshot_tx,
            true,
            pending.len(),
            active.len(),
            records.len(),
            report.terminal_count(),
        );

        tokio::select! {
            () = shutdown_request.cancelled() => {
                accepting = false;
            }

            submission = submissions.recv() => {
                match submission {
                    Some(submission) => handle_submission(
                        submission,
                        limits,
                        active.len(),
                        &mut pending,
                        &mut records,
                        &mut report,
                    ),
                    None => accepting = false,
                }
            }

            joined = active.join_next_with_id(), if !active.is_empty() => {
                if let Some(joined) = joined {
                    complete_join(joined, &mut active_keys, &mut records, &mut report);
                }
            }
        }
    }

    // Stop admission before signalling or cancelling committed work.
    submissions.close();
    while let Ok(submission) = submissions.try_recv() {
        let _ = submission.reply.send(Reply::ShuttingDown);
    }
    publish(
        &snapshot_tx,
        false,
        pending.len(),
        active.len(),
        records.len(),
        report.terminal_count(),
    );

    // Pending work committed to the actor but never started receives an
    // explicit terminal cancellation.
    while let Some(pending) = pending.pop_front() {
        complete_record(
            &pending.key,
            Reply::Cancelled,
            &mut records,
            &mut report,
        );
    }

    child_cancel.cancel();
    let deadline = time::Instant::now() + limits.shutdown_grace;

    while !active.is_empty() {
        match time::timeout_at(deadline, active.join_next_with_id()).await {
            Ok(Some(joined)) => {
                complete_join(joined, &mut active_keys, &mut records, &mut report);
            }
            Ok(None) => break,
            Err(_) => break,
        }
    }

    if !active.is_empty() {
        active.abort_all();
        while let Some(joined) = active.join_next_with_id().await {
            complete_join(joined, &mut active_keys, &mut records, &mut report);
        }
    }

    debug_assert!(active_keys.is_empty());
    debug_assert_eq!(report.committed, report.terminal_count());
    publish(
        &snapshot_tx,
        false,
        0,
        0,
        records.len(),
        report.terminal_count(),
    );
    report
}

fn handle_submission(
    submission: Submit,
    limits: Limits,
    active_count: usize,
    pending: &mut VecDeque<Pending>,
    records: &mut HashMap<String, Record>,
    report: &mut Report,
) {
    if let Some(record) = records.get_mut(&submission.key) {
        if record.recipient != submission.recipient {
            let _ = submission.reply.send(Reply::Conflict);
            return;
        }

        match &mut record.state {
            RecordState::Completed(outcome) => {
                let _ = submission.reply.send(outcome.clone());
            }
            RecordState::InProgress { waiters } => {
                if waiters.len() >= limits.waiters_per_key {
                    let _ = submission.reply.send(Reply::Busy);
                } else {
                    waiters.push(submission.reply);
                }
            }
        }
        return;
    }

    if records.len() >= limits.records {
        let _ = submission.reply.send(Reply::Busy);
        return;
    }

    let has_work_capacity = active_count < limits.active || pending.len() < limits.pending;
    if !has_work_capacity {
        let _ = submission.reply.send(Reply::Busy);
        return;
    }

    let previous = records.insert(
        submission.key.clone(),
        Record {
            recipient: submission.recipient.clone(),
            state: RecordState::InProgress {
                waiters: vec![submission.reply],
            },
        },
    );
    debug_assert!(previous.is_none());
    pending.push_back(Pending {
        key: submission.key,
        recipient: submission.recipient,
    });
    report.committed += 1;
}

fn start_ready_deliveries(
    active_limit: usize,
    pending: &mut VecDeque<Pending>,
    active: &mut JoinSet<DeliveryExit>,
    active_keys: &mut HashMap<Id, String>,
    child_cancel: &CancellationToken,
    report: &mut Report,
) {
    while active.len() < active_limit {
        let Some(pending) = pending.pop_front() else {
            break;
        };

        let key = pending.key;
        let token = child_cancel.child_token();
        let abort_handle = active.spawn(deliver(pending.recipient, token));
        debug_assert!(active_keys.insert(abort_handle.id(), key).is_none());
        report.executions += 1;
    }
}

fn complete_join(
    joined: Result<(Id, DeliveryExit), tokio::task::JoinError>,
    active_keys: &mut HashMap<Id, String>,
    records: &mut HashMap<String, Record>,
    report: &mut Report,
) {
    match joined {
        Ok((task_id, exit)) => {
            let key = active_keys
                .remove(&task_id)
                .expect("every active delivery must retain its semantic key");
            let outcome = match exit {
                DeliveryExit::Delivered => Reply::Delivered,
                DeliveryExit::Failed(message) => Reply::Failed(message),
                DeliveryExit::Cancelled => Reply::Cancelled,
            };
            complete_record(&key, outcome, records, report);
        }
        Err(join_error) => {
            let task_id = join_error.id();
            let key = active_keys
                .remove(&task_id)
                .expect("every failed delivery join must retain its semantic key");
            let outcome = if join_error.is_cancelled() {
                Reply::Cancelled
            } else {
                Reply::Panicked
            };
            complete_record(&key, outcome, records, report);
        }
    }
}

fn complete_record(
    key: &str,
    outcome: Reply,
    records: &mut HashMap<String, Record>,
    report: &mut Report,
) {
    let record = records
        .get_mut(key)
        .expect("every committed key must retain an idempotency record");

    let waiters = match &mut record.state {
        RecordState::InProgress { waiters } => std::mem::take(waiters),
        RecordState::Completed(_) => return,
    };
    record.state = RecordState::Completed(outcome.clone());

    for waiter in waiters {
        let _ = waiter.send(outcome.clone());
    }
    debug_assert!(report.outcomes.insert(key.to_owned(), outcome).is_none());
}

async fn deliver(recipient: String, cancel: CancellationToken) -> DeliveryExit {
    if let Some(rest) = recipient.strip_prefix("panic:") {
        panic!("injected delivery panic for {rest}");
    }

    if let Some((delay, address)) = parse_delayed(&recipient, "stubborn:") {
        time::sleep(delay).await;
        return validate_recipient(address);
    }

    if let Some((delay, address)) = parse_delayed(&recipient, "slow:") {
        return tokio::select! {
            () = cancel.cancelled() => DeliveryExit::Cancelled,
            () = time::sleep(delay) => validate_recipient(address),
        };
    }

    if let Some(message) = recipient.strip_prefix("fail:") {
        return DeliveryExit::Failed(message.to_owned());
    }

    tokio::select! {
        () = cancel.cancelled() => DeliveryExit::Cancelled,
        () = tokio::task::yield_now() => validate_recipient(&recipient),
    }
}

fn parse_delayed<'a>(value: &'a str, prefix: &str) -> Option<(Duration, &'a str)> {
    let rest = value.strip_prefix(prefix)?;
    let (millis, address) = rest.split_once(':')?;
    let millis = millis.parse::<u64>().ok()?;
    Some((Duration::from_millis(millis), address))
}

fn validate_recipient(recipient: &str) -> DeliveryExit {
    if recipient.contains('@') && !recipient.starts_with('@') && !recipient.ends_with('@') {
        DeliveryExit::Delivered
    } else {
        DeliveryExit::Failed("recipient is not a valid local email-shaped address".to_owned())
    }
}

fn validate_submission(key: &str, recipient: &str) -> Result<(), &'static str> {
    if key.is_empty() || key.len() > 32 {
        return Err("key must contain 1..=32 bytes");
    }
    if !key
        .bytes()
        .all(|byte| byte.is_ascii_alphanumeric() || matches!(byte, b'-' | b'_'))
    {
        return Err("key contains unsupported characters");
    }
    if recipient.is_empty() || recipient.len() > 256 {
        return Err("recipient must contain 1..=256 bytes");
    }
    Ok(())
}

fn publish(
    snapshot_tx: &watch::Sender<Snapshot>,
    accepting: bool,
    pending: usize,
    active: usize,
    records: usize,
    terminal: usize,
) {
    let _previous = snapshot_tx.send_replace(Snapshot {
        accepting,
        pending,
        active,
        records,
        terminal,
    });
}

#[cfg(test)]
mod tests {
    use super::*;
    use tokio::task;

    fn limits() -> Limits {
        Limits {
            mailbox: 8,
            pending: 1,
            active: 1,
            records: 8,
            waiters_per_key: 2,
            shutdown_grace: Duration::from_secs(2),
        }
    }

    #[tokio::test(start_paused = true)]
    async fn duplicate_during_delivery_shares_one_execution() {
        let (service, dispatcher) = start(limits()).unwrap();

        let first = task::spawn({
            let service = service.clone();
            async move { service.submit("same", "slow:1000:a@example.test").await }
        });
        task::yield_now().await;
        task::yield_now().await;

        let duplicate = task::spawn({
            let service = service.clone();
            async move { service.submit("same", "slow:1000:a@example.test").await }
        });
        task::yield_now().await;

        time::advance(Duration::from_secs(1)).await;
        assert_eq!(first.await.unwrap(), Reply::Delivered);
        assert_eq!(duplicate.await.unwrap(), Reply::Delivered);

        assert_eq!(
            service.submit("same", "changed@example.test").await,
            Reply::Conflict
        );

        service.request_shutdown();
        let report = dispatcher.await.unwrap();
        assert_eq!(report.committed, 1);
        assert_eq!(report.executions, 1);
        assert_eq!(report.outcomes["same"], Reply::Delivered);
    }

    #[tokio::test(start_paused = true)]
    async fn active_and_pending_limits_reject_before_commit() {
        let (service, dispatcher) = start(limits()).unwrap();

        let active = task::spawn({
            let service = service.clone();
            async move { service.submit("active", "slow:1000:a@example.test").await }
        });
        task::yield_now().await;
        task::yield_now().await;

        let pending = task::spawn({
            let service = service.clone();
            async move { service.submit("pending", "slow:1000:b@example.test").await }
        });
        task::yield_now().await;
        task::yield_now().await;

        let snapshot = service.snapshot();
        assert_eq!(snapshot.active, 1);
        assert_eq!(snapshot.pending, 1);
        assert_eq!(service.submit("overflow", "c@example.test").await, Reply::Busy);

        time::advance(Duration::from_secs(1)).await;
        task::yield_now().await;
        time::advance(Duration::from_secs(1)).await;
        assert_eq!(active.await.unwrap(), Reply::Delivered);
        assert_eq!(pending.await.unwrap(), Reply::Delivered);

        service.request_shutdown();
        let report = dispatcher.await.unwrap();
        assert_eq!(report.committed, 2);
        assert_eq!(report.terminal_count(), 2);
    }

    #[tokio::test(start_paused = true)]
    async fn shutdown_cancels_pending_and_aborts_stubborn_active_work() {
        let (service, dispatcher) = start(limits()).unwrap();

        let stubborn = task::spawn({
            let service = service.clone();
            async move {
                service
                    .submit("stubborn", "stubborn:100000:a@example.test")
                    .await
            }
        });
        task::yield_now().await;
        task::yield_now().await;

        let queued = task::spawn({
            let service = service.clone();
            async move { service.submit("queued", "b@example.test").await }
        });
        task::yield_now().await;
        task::yield_now().await;

        service.request_shutdown();
        task::yield_now().await;
        assert_eq!(queued.await.unwrap(), Reply::Cancelled);

        time::advance(Duration::from_secs(3)).await;
        assert_eq!(stubborn.await.unwrap(), Reply::Cancelled);

        let report = dispatcher.await.unwrap();
        assert_eq!(report.outcomes["queued"], Reply::Cancelled);
        assert_eq!(report.outcomes["stubborn"], Reply::Cancelled);
        assert_eq!(report.committed, report.terminal_count());
    }

    #[tokio::test(start_paused = true)]
    async fn task_panic_becomes_a_terminal_semantic_outcome() {
        let (service, dispatcher) = start(limits()).unwrap();

        let request = task::spawn({
            let service = service.clone();
            async move { service.submit("panic", "panic:a@example.test").await }
        });
        task::yield_now().await;
        task::yield_now().await;
        assert_eq!(request.await.unwrap(), Reply::Panicked);

        service.request_shutdown();
        let report = dispatcher.await.unwrap();
        assert_eq!(report.outcomes["panic"], Reply::Panicked);
    }

    #[tokio::test]
    async fn invalid_request_never_commits() {
        let (service, dispatcher) = start(limits()).unwrap();
        assert!(matches!(service.submit("", "a@example.test").await, Reply::Invalid(_)));

        service.request_shutdown();
        let report = dispatcher.await.unwrap();
        assert_eq!(report.committed, 0);
        assert_eq!(report.terminal_count(), 0);
    }
}
