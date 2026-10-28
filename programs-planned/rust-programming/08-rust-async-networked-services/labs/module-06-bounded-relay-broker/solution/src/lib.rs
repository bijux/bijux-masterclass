//! A bounded, actor-owned relay broker.
//!
//! The bounded mailbox limits requests waiting to be inspected. The actor's
//! FIFO limits committed work waiting for execution. `JoinSet::len` limits
//! active jobs. These are different resources and are therefore represented
//! by different fields.

use std::{collections::VecDeque, time::Duration};

use tokio::{
    sync::{mpsc, oneshot, watch},
    task::{JoinHandle, JoinSet},
    time,
};
use tokio_util::sync::CancellationToken;

const SIMULATED_JOB_LATENCY: Duration = Duration::from_millis(10);

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Limits {
    pub mailbox: usize,
    pub queued: usize,
    pub active: usize,
}

impl Limits {
    pub fn validate(self) -> Result<Self, ConfigError> {
        if self.mailbox == 0 {
            return Err(ConfigError::ZeroMailbox);
        }
        if self.queued == 0 {
            return Err(ConfigError::ZeroQueue);
        }
        if self.active == 0 {
            return Err(ConfigError::ZeroActive);
        }
        Ok(self)
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ConfigError {
    ZeroMailbox,
    ZeroQueue,
    ZeroActive,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Reply {
    Value(u64),
    Busy,
    Failed(String),
    Cancelled,
}

#[derive(Debug, Clone, PartialEq, Eq, Default)]
pub struct Snapshot {
    pub queued: usize,
    pub active: usize,
    pub committed: u64,
    pub completed: u64,
}

#[derive(Debug, Clone, PartialEq, Eq, Default)]
pub struct RunReport {
    pub committed: u64,
    pub completed: u64,
    pub rejected: u64,
    pub cancelled_before_start: u64,
}

struct Request {
    input: u64,
    reply: oneshot::Sender<Reply>,
}

struct Pending {
    input: u64,
    reply: oneshot::Sender<Reply>,
}

#[derive(Clone)]
pub struct Broker {
    requests: mpsc::Sender<Request>,
    snapshot: watch::Receiver<Snapshot>,
}

impl Broker {
    /// Attempts admission without waiting for mailbox capacity.
    ///
    /// `Busy` here means the request did not commit. Once the actor accepts the
    /// request into its waiting queue or active set, the caller receives one
    /// terminal reply even if shutdown begins later.
    pub async fn submit(&self, input: u64) -> Reply {
        let (reply_tx, reply_rx) = oneshot::channel();
        let request = Request {
            input,
            reply: reply_tx,
        };

        match self.requests.try_send(request) {
            Ok(()) => {}
            Err(mpsc::error::TrySendError::Full(_)) => return Reply::Busy,
            Err(mpsc::error::TrySendError::Closed(_)) => return Reply::Cancelled,
        }

        reply_rx.await.unwrap_or(Reply::Cancelled)
    }

    pub fn snapshot(&self) -> Snapshot {
        self.snapshot.borrow().clone()
    }
}

pub fn start(
    limits: Limits,
    cancel: CancellationToken,
) -> Result<(Broker, JoinHandle<RunReport>), ConfigError> {
    let limits = limits.validate()?;
    let (request_tx, request_rx) = mpsc::channel(limits.mailbox);
    let (snapshot_tx, snapshot_rx) = watch::channel(Snapshot::default());

    let task = tokio::spawn(run_actor(limits, cancel, request_rx, snapshot_tx));
    Ok((
        Broker {
            requests: request_tx,
            snapshot: snapshot_rx,
        },
        task,
    ))
}

async fn run_actor(
    limits: Limits,
    cancel: CancellationToken,
    mut requests: mpsc::Receiver<Request>,
    snapshot_tx: watch::Sender<Snapshot>,
) -> RunReport {
    let mut waiting = VecDeque::<Pending>::new();
    let mut active = JoinSet::new();
    let mut receiver_open = true;
    let mut shutdown_started = false;
    let mut report = RunReport::default();

    loop {
        while active.len() < limits.active {
            let Some(pending) = waiting.pop_front() else {
                break;
            };

            let _abort_handle = active.spawn(async move {
                let result = execute(pending.input).await;
                (pending.reply, result)
            });
        }

        let _previous = snapshot_tx.send_replace(Snapshot {
            queued: waiting.len(),
            active: active.len(),
            committed: report.committed,
            completed: report.completed,
        });

        if !receiver_open && waiting.is_empty() && active.is_empty() {
            break;
        }

        tokio::select! {
            () = cancel.cancelled(), if !shutdown_started => {
                shutdown_started = true;
                receiver_open = false;
                requests.close();

                while let Ok(request) = requests.try_recv() {
                    let _ = request.reply.send(Reply::Cancelled);
                    report.cancelled_before_start += 1;
                }
                while let Some(pending) = waiting.pop_front() {
                    let _ = pending.reply.send(Reply::Cancelled);
                    report.cancelled_before_start += 1;
                }
            }

            request = requests.recv(), if receiver_open => {
                match request {
                    Some(request) => {
                        let can_commit = active.len() < limits.active
                            || waiting.len() < limits.queued;

                        if can_commit {
                            waiting.push_back(Pending {
                                input: request.input,
                                reply: request.reply,
                            });
                            report.committed += 1;
                        } else {
                            let _ = request.reply.send(Reply::Busy);
                            report.rejected += 1;
                        }
                    }
                    None => {
                        receiver_open = false;
                    }
                }
            }

            joined = active.join_next(), if !active.is_empty() => {
                match joined {
                    Some(Ok((reply, result))) => {
                        // Active capacity is released when the task leaves the
                        // JoinSet, before the terminal reply is sent.
                        report.completed += 1;
                        let terminal = match result {
                            Ok(value) => Reply::Value(value),
                            Err(message) => Reply::Failed(message),
                        };
                        let _ = reply.send(terminal);
                    }
                    Some(Err(join_error)) => {
                        // `execute` contains no panic path. Reaching this branch
                        // would violate the laboratory's worker contract. The
                        // actor remains alive and records the lost completion.
                        report.completed += 1;
                        report.rejected += 1;
                        debug_assert!(join_error.is_panic() || join_error.is_cancelled());
                    }
                    None => {}
                }
            }
        }
    }

    let _previous = snapshot_tx.send_replace(Snapshot {
        queued: 0,
        active: 0,
        committed: report.committed,
        completed: report.completed,
    });
    report
}

async fn execute(input: u64) -> Result<u64, String> {
    time::sleep(SIMULATED_JOB_LATENCY).await;
    input
        .checked_mul(2)
        .ok_or_else(|| "doubling the input overflowed u64".to_owned())
}

#[cfg(test)]
mod tests {
    use super::*;
    use tokio::task;

    fn limits() -> Limits {
        Limits {
            mailbox: 8,
            queued: 1,
            active: 1,
        }
    }

    #[test]
    fn zero_capacity_is_rejected() {
        assert_eq!(
            Limits {
                mailbox: 1,
                queued: 0,
                active: 1,
            }
            .validate(),
            Err(ConfigError::ZeroQueue)
        );
    }

    #[tokio::test(start_paused = true)]
    async fn committed_work_receives_one_terminal_reply() {
        let cancel = CancellationToken::new();
        let (broker, actor) = start(limits(), cancel.clone()).unwrap();

        let request = task::spawn({
            let broker = broker.clone();
            async move { broker.submit(21).await }
        });
        task::yield_now().await;
        time::advance(SIMULATED_JOB_LATENCY).await;

        assert_eq!(request.await.unwrap(), Reply::Value(42));
        assert_eq!(broker.snapshot().completed, 1);

        cancel.cancel();
        let report = actor.await.unwrap();
        assert_eq!(report.committed, 1);
        assert_eq!(report.completed, 1);
    }

    #[tokio::test(start_paused = true)]
    async fn active_and_waiting_capacity_are_independently_bounded() {
        let cancel = CancellationToken::new();
        let (broker, actor) = start(limits(), cancel.clone()).unwrap();

        let first = task::spawn({
            let broker = broker.clone();
            async move { broker.submit(1).await }
        });
        task::yield_now().await;
        task::yield_now().await;

        let second = task::spawn({
            let broker = broker.clone();
            async move { broker.submit(2).await }
        });
        task::yield_now().await;
        task::yield_now().await;

        let snapshot = broker.snapshot();
        assert_eq!(snapshot.active, 1);
        assert_eq!(snapshot.queued, 1);

        let third = broker.submit(3).await;
        assert_eq!(third, Reply::Busy);

        time::advance(SIMULATED_JOB_LATENCY).await;
        task::yield_now().await;
        time::advance(SIMULATED_JOB_LATENCY).await;

        assert_eq!(first.await.unwrap(), Reply::Value(2));
        assert_eq!(second.await.unwrap(), Reply::Value(4));

        cancel.cancel();
        actor.await.unwrap();
    }

    #[tokio::test(start_paused = true)]
    async fn dropped_reply_receiver_does_not_hold_active_capacity() {
        let cancel = CancellationToken::new();
        let (broker, actor) = start(limits(), cancel.clone()).unwrap();

        let abandoned = task::spawn({
            let broker = broker.clone();
            async move { broker.submit(4).await }
        });
        task::yield_now().await;
        abandoned.abort();

        time::advance(SIMULATED_JOB_LATENCY).await;
        task::yield_now().await;

        let next = task::spawn({
            let broker = broker.clone();
            async move { broker.submit(5).await }
        });
        task::yield_now().await;
        time::advance(SIMULATED_JOB_LATENCY).await;
        assert_eq!(next.await.unwrap(), Reply::Value(10));

        cancel.cancel();
        actor.await.unwrap();
    }

    #[tokio::test(start_paused = true)]
    async fn shutdown_cancels_waiting_work_but_drains_active_work() {
        let cancel = CancellationToken::new();
        let (broker, actor) = start(limits(), cancel.clone()).unwrap();

        let active = task::spawn({
            let broker = broker.clone();
            async move { broker.submit(6).await }
        });
        task::yield_now().await;
        task::yield_now().await;

        let waiting = task::spawn({
            let broker = broker.clone();
            async move { broker.submit(7).await }
        });
        task::yield_now().await;
        task::yield_now().await;

        cancel.cancel();
        task::yield_now().await;
        assert_eq!(waiting.await.unwrap(), Reply::Cancelled);

        time::advance(SIMULATED_JOB_LATENCY).await;
        assert_eq!(active.await.unwrap(), Reply::Value(12));

        let report = actor.await.unwrap();
        assert_eq!(report.committed, 2);
        assert_eq!(report.completed, 1);
        assert_eq!(report.cancelled_before_start, 1);
    }
}
