//! A dynamic, join-bounded task supervisor.
//!
//! A shutdown request is not the report. It begins one ordered transition:
//!
//! 1. close admission;
//! 2. reject commands already buffered but not accepted;
//! 3. cancel the child token;
//! 4. drain until one absolute grace deadline;
//! 5. abort leftovers;
//! 6. join every remaining handle;
//! 7. return one terminal outcome per accepted semantic task id.

use std::{
    collections::{BTreeMap, HashMap, HashSet},
    future::Future,
    pin::Pin,
    time::Duration,
};

use tokio::{
    sync::{mpsc, oneshot, watch},
    task::{Id, JoinHandle, JoinSet},
    time,
};
use tokio_util::sync::CancellationToken;

type BoxTask = Pin<Box<dyn Future<Output = ChildExit> + Send + 'static>>;
type TaskFactory = Box<dyn FnOnce(CancellationToken) -> BoxTask + Send + 'static>;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ChildExit {
    Completed,
    Failed(String),
    Cancelled,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Outcome {
    Completed,
    Failed(String),
    Panicked,
    Cancelled,
}

#[derive(Debug, Default, Clone, PartialEq, Eq)]
pub struct Report {
    pub outcomes: BTreeMap<String, Outcome>,
}

impl Report {
    pub fn total(&self) -> usize {
        self.outcomes.len()
    }

    pub fn completed(&self) -> usize {
        self.outcomes
            .values()
            .filter(|outcome| matches!(outcome, Outcome::Completed))
            .count()
    }

    pub fn failed(&self) -> usize {
        self.outcomes
            .values()
            .filter(|outcome| matches!(outcome, Outcome::Failed(_)))
            .count()
    }

    pub fn panicked(&self) -> usize {
        self.outcomes
            .values()
            .filter(|outcome| matches!(outcome, Outcome::Panicked))
            .count()
    }

    pub fn cancelled(&self) -> usize {
        self.outcomes
            .values()
            .filter(|outcome| matches!(outcome, Outcome::Cancelled))
            .count()
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Default)]
pub struct Snapshot {
    pub accepting: bool,
    pub active: usize,
    pub terminal: usize,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ConfigError {
    ZeroMailbox,
    ZeroGrace,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum SubmitError {
    Busy,
    DuplicateId,
    ShuttingDown,
    SupervisorStopped,
}

enum Command {
    Spawn {
        id: String,
        factory: TaskFactory,
        accepted: oneshot::Sender<Result<(), SubmitError>>,
    },
}

#[derive(Clone)]
pub struct Supervisor {
    commands: mpsc::Sender<Command>,
    shutdown_request: CancellationToken,
    snapshot: watch::Receiver<Snapshot>,
}

impl Supervisor {
    pub async fn submit<F, Fut>(&self, id: impl Into<String>, factory: F) -> Result<(), SubmitError>
    where
        F: FnOnce(CancellationToken) -> Fut + Send + 'static,
        Fut: Future<Output = ChildExit> + Send + 'static,
    {
        if self.shutdown_request.is_cancelled() {
            return Err(SubmitError::ShuttingDown);
        }

        let (accepted_tx, accepted_rx) = oneshot::channel();
        let factory: TaskFactory = Box::new(move |token| Box::pin(factory(token)));
        let command = Command::Spawn {
            id: id.into(),
            factory,
            accepted: accepted_tx,
        };

        match self.commands.try_send(command) {
            Ok(()) => {}
            Err(mpsc::error::TrySendError::Full(_)) => return Err(SubmitError::Busy),
            Err(mpsc::error::TrySendError::Closed(_)) => {
                return Err(SubmitError::SupervisorStopped);
            }
        }

        accepted_rx
            .await
            .unwrap_or(Err(SubmitError::SupervisorStopped))
    }

    /// Requests shutdown. Calling this method repeatedly is harmless.
    pub fn request_shutdown(&self) {
        self.shutdown_request.cancel();
    }

    pub fn snapshot(&self) -> Snapshot {
        self.snapshot.borrow().clone()
    }
}

pub fn start(
    mailbox_capacity: usize,
    grace: Duration,
) -> Result<(Supervisor, JoinHandle<Report>), ConfigError> {
    if mailbox_capacity == 0 {
        return Err(ConfigError::ZeroMailbox);
    }
    if grace.is_zero() {
        return Err(ConfigError::ZeroGrace);
    }

    let (command_tx, command_rx) = mpsc::channel(mailbox_capacity);
    let shutdown_request = CancellationToken::new();
    let (snapshot_tx, snapshot_rx) = watch::channel(Snapshot {
        accepting: true,
        active: 0,
        terminal: 0,
    });

    let task = tokio::spawn(run_supervisor(
        command_rx,
        shutdown_request.clone(),
        grace,
        snapshot_tx,
    ));

    Ok((
        Supervisor {
            commands: command_tx,
            shutdown_request,
            snapshot: snapshot_rx,
        },
        task,
    ))
}

async fn run_supervisor(
    mut commands: mpsc::Receiver<Command>,
    shutdown_request: CancellationToken,
    grace: Duration,
    snapshot_tx: watch::Sender<Snapshot>,
) -> Report {
    let child_cancel = CancellationToken::new();
    let mut tasks = JoinSet::<ChildExit>::new();
    let mut active_ids = HashMap::<Id, String>::new();
    let mut accepted_ids = HashSet::<String>::new();
    let mut report = Report::default();
    let mut accepting = true;

    while accepting {
        publish(&snapshot_tx, true, tasks.len(), report.total());

        tokio::select! {
            () = shutdown_request.cancelled() => {
                accepting = false;
            }

            command = commands.recv() => {
                match command {
                    Some(Command::Spawn { id, factory, accepted }) => {
                        if accepted_ids.contains(&id) {
                            let _ = accepted.send(Err(SubmitError::DuplicateId));
                            continue;
                        }

                        debug_assert!(accepted_ids.insert(id.clone()));
                        let future = factory(child_cancel.child_token());
                        let abort_handle = tasks.spawn(future);
                        debug_assert!(active_ids.insert(abort_handle.id(), id).is_none());
                        let _ = accepted.send(Ok(()));
                    }
                    None => {
                        accepting = false;
                    }
                }
            }

            joined = tasks.join_next_with_id(), if !tasks.is_empty() => {
                if let Some(joined) = joined {
                    record_join(joined, &mut active_ids, &mut report);
                }
            }
        }
    }

    // Admission closes before cancellation is propagated.
    commands.close();
    while let Ok(command) = commands.try_recv() {
        match command {
            Command::Spawn { accepted, .. } => {
                let _ = accepted.send(Err(SubmitError::ShuttingDown));
            }
        }
    }
    publish(&snapshot_tx, false, tasks.len(), report.total());

    child_cancel.cancel();
    let deadline = time::Instant::now() + grace;

    while !tasks.is_empty() {
        match time::timeout_at(deadline, tasks.join_next_with_id()).await {
            Ok(Some(joined)) => {
                record_join(joined, &mut active_ids, &mut report);
                publish(&snapshot_tx, false, tasks.len(), report.total());
            }
            Ok(None) => break,
            Err(_) => break,
        }
    }

    if !tasks.is_empty() {
        tasks.abort_all();
        while let Some(joined) = tasks.join_next_with_id().await {
            record_join(joined, &mut active_ids, &mut report);
        }
    }

    debug_assert!(active_ids.is_empty());
    debug_assert_eq!(report.total(), accepted_ids.len());
    publish(&snapshot_tx, false, 0, report.total());
    report
}

fn publish(
    snapshot_tx: &watch::Sender<Snapshot>,
    accepting: bool,
    active: usize,
    terminal: usize,
) {
    let _previous = snapshot_tx.send_replace(Snapshot {
        accepting,
        active,
        terminal,
    });
}

fn record_join(
    joined: Result<(Id, ChildExit), tokio::task::JoinError>,
    active_ids: &mut HashMap<Id, String>,
    report: &mut Report,
) {
    match joined {
        Ok((task_id, exit)) => {
            let semantic_id = active_ids
                .remove(&task_id)
                .expect("every joined task must have a semantic id");
            let outcome = match exit {
                ChildExit::Completed => Outcome::Completed,
                ChildExit::Failed(message) => Outcome::Failed(message),
                ChildExit::Cancelled => Outcome::Cancelled,
            };
            debug_assert!(report.outcomes.insert(semantic_id, outcome).is_none());
        }
        Err(error) => {
            let task_id = error.id();
            let semantic_id = active_ids
                .remove(&task_id)
                .expect("every failed join must have a semantic id");
            let outcome = if error.is_cancelled() {
                Outcome::Cancelled
            } else {
                Outcome::Panicked
            };
            debug_assert!(report.outcomes.insert(semantic_id, outcome).is_none());
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use tokio::task;

    #[tokio::test(start_paused = true)]
    async fn completed_and_failed_tasks_keep_their_real_outcome() {
        let (supervisor, task) = start(8, Duration::from_secs(5)).unwrap();

        supervisor
            .submit("completed", |_| async { ChildExit::Completed })
            .await
            .unwrap();
        supervisor
            .submit("failed", |_| async {
                ChildExit::Failed("domain rejection".to_owned())
            })
            .await
            .unwrap();

        task::yield_now().await;
        supervisor.request_shutdown();
        let report = task.await.unwrap();

        assert_eq!(report.outcomes["completed"], Outcome::Completed);
        assert_eq!(
            report.outcomes["failed"],
            Outcome::Failed("domain rejection".to_owned())
        );
    }

    #[tokio::test(start_paused = true)]
    async fn panic_is_not_erased_into_cancellation() {
        let (supervisor, task) = start(8, Duration::from_secs(5)).unwrap();

        supervisor
            .submit("panics", |_| async { panic!("injected child panic") })
            .await
            .unwrap();
        task::yield_now().await;
        supervisor.request_shutdown();

        let report = task.await.unwrap();
        assert_eq!(report.outcomes["panics"], Outcome::Panicked);
    }

    #[tokio::test(start_paused = true)]
    async fn duplicate_semantic_identity_is_rejected() {
        let (supervisor, task) = start(8, Duration::from_secs(5)).unwrap();

        supervisor
            .submit("same-id", |_| async { ChildExit::Completed })
            .await
            .unwrap();
        let duplicate = supervisor
            .submit("same-id", |_| async { ChildExit::Completed })
            .await;
        assert_eq!(duplicate, Err(SubmitError::DuplicateId));

        supervisor.request_shutdown();
        assert_eq!(task.await.unwrap().total(), 1);
    }

    #[tokio::test(start_paused = true)]
    async fn grace_expiry_aborts_a_task_that_ignores_cancellation() {
        let (supervisor, task) = start(8, Duration::from_secs(5)).unwrap();

        supervisor
            .submit("stubborn", |_cancel| async {
                time::sleep(Duration::from_secs(100)).await;
                ChildExit::Completed
            })
            .await
            .unwrap();

        supervisor.request_shutdown();
        supervisor.request_shutdown();
        task::yield_now().await;
        time::advance(Duration::from_secs(6)).await;

        let report = task.await.unwrap();
        assert_eq!(report.outcomes["stubborn"], Outcome::Cancelled);
        assert_eq!(report.total(), 1);
    }

    #[tokio::test(start_paused = true)]
    async fn cooperative_child_can_finish_inside_grace() {
        let (supervisor, task) = start(8, Duration::from_secs(5)).unwrap();

        supervisor
            .submit("cooperative", |cancel| async move {
                cancel.cancelled().await;
                time::sleep(Duration::from_secs(2)).await;
                ChildExit::Cancelled
            })
            .await
            .unwrap();

        supervisor.request_shutdown();
        task::yield_now().await;
        time::advance(Duration::from_secs(2)).await;

        let report = task.await.unwrap();
        assert_eq!(report.outcomes["cooperative"], Outcome::Cancelled);
    }
}
