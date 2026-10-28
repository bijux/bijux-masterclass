#![forbid(unsafe_code)]

use std::collections::VecDeque;
use std::panic::{self, AssertUnwindSafe};
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::mpsc;
use std::sync::{Arc, Condvar, Mutex};
use std::thread;

pub const MAX_TASKS: usize = 1024;
pub const MAX_WORKERS: usize = 64;
pub const MAX_CAPACITY: usize = 1024;
pub const MAX_TOTAL_TEXT_BYTES: usize = 1024 * 1024;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum TaskMode {
    Normal,
    DomainFail,
    Panic,
    Spin(usize),
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Task {
    pub index: usize,
    pub text: String,
    pub mode: TaskMode,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum TaskOutcome {
    Completed { index: usize, value: String },
    Failed { index: usize, message: String },
    Panicked { index: usize },
    Cancelled { index: usize },
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum FailurePolicy {
    Continue,
    FailFast,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum RunError {
    ZeroWorkers,
    TooManyWorkers { count: usize, limit: usize },
    ZeroCapacity,
    CapacityTooLarge { count: usize, limit: usize },
    TooManyTasks { count: usize, limit: usize },
    TooManyTextBytes { count: usize, limit: usize },
    InvalidTaskIndex { position: usize, observed: usize },
    OutcomeOutOfRange { index: usize, count: usize },
    DuplicateOutcome { index: usize },
    MissingOutcome { index: usize },
    WorkerPanicked { worker: usize },
}

struct QueueState<T> {
    items: VecDeque<T>,
    closed: bool,
}

struct Queue<T> {
    capacity: usize,
    state: Mutex<QueueState<T>>,
    not_empty: Condvar,
    not_full: Condvar,
}

impl<T> Queue<T> {
    fn new(capacity: usize) -> Self {
        Self {
            capacity,
            state: Mutex::new(QueueState {
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

enum Execution {
    Completed(String),
    Failed(String),
    Cancelled,
}

fn execute(task: &Task, cancelled: &AtomicBool) -> Execution {
    match task.mode {
        TaskMode::Normal => Execution::Completed(task.text.to_uppercase()),
        TaskMode::DomainFail => Execution::Failed("injected domain failure".to_owned()),
        TaskMode::Panic => panic!("injected task panic"),
        TaskMode::Spin(steps) => {
            for _ in 0..steps {
                if cancelled.load(Ordering::Relaxed) {
                    return Execution::Cancelled;
                }
                thread::yield_now();
            }
            Execution::Completed(task.text.to_uppercase())
        }
    }
}

pub fn run(
    tasks: Vec<Task>,
    workers: usize,
    capacity: usize,
    policy: FailurePolicy,
) -> Result<Vec<TaskOutcome>, RunError> {
    validate_inputs(&tasks, workers, capacity)?;

    let count = tasks.len();
    let queue = Arc::new(Queue::new(capacity));
    let cancelled = Arc::new(AtomicBool::new(false));
    let (result_tx, result_rx) = mpsc::channel::<TaskOutcome>();
    let mut handles = Vec::with_capacity(workers);

    for worker in 0..workers {
        let queue = Arc::clone(&queue);
        let cancelled = Arc::clone(&cancelled);
        let result_tx = result_tx.clone();
        handles.push((
            worker,
            thread::spawn(move || {
                while let Some(task) = queue.pop() {
                    let index = task.index;
                    let outcome = if cancelled.load(Ordering::Relaxed) {
                        TaskOutcome::Cancelled { index }
                    } else {
                        let execution = panic::catch_unwind(AssertUnwindSafe(|| {
                            execute(&task, &cancelled)
                        }));
                        match execution {
                            Ok(Execution::Completed(value)) => {
                                TaskOutcome::Completed { index, value }
                            }
                            Ok(Execution::Cancelled) => TaskOutcome::Cancelled { index },
                            Ok(Execution::Failed(message)) => {
                                if policy == FailurePolicy::FailFast {
                                    cancelled.store(true, Ordering::Relaxed);
                                    queue.close();
                                }
                                TaskOutcome::Failed { index, message }
                            }
                            Err(_) => {
                                if policy == FailurePolicy::FailFast {
                                    cancelled.store(true, Ordering::Relaxed);
                                    queue.close();
                                }
                                TaskOutcome::Panicked { index }
                            }
                        }
                    };

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
    let mut iterator = tasks.into_iter();
    while let Some(task) = iterator.next() {
        match queue.push(task) {
            Ok(()) => {}
            Err(task) => {
                rejected.push(task);
                rejected.extend(iterator);
                break;
            }
        }
    }
    queue.close();

    let mut slots: Vec<Option<TaskOutcome>> = (0..count).map(|_| None).collect();
    let mut protocol_error = None;
    for outcome in result_rx {
        let index = outcome_index(&outcome);
        let Some(slot) = slots.get_mut(index) else {
            protocol_error.get_or_insert(RunError::OutcomeOutOfRange { index, count });
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

    for task in rejected {
        let slot = &mut slots[task.index];
        if slot.is_some() {
            return Err(RunError::DuplicateOutcome { index: task.index });
        }
        *slot = Some(TaskOutcome::Cancelled { index: task.index });
    }

    slots
        .into_iter()
        .enumerate()
        .map(|(index, outcome)| outcome.ok_or(RunError::MissingOutcome { index }))
        .collect()
}

fn validate_inputs(tasks: &[Task], workers: usize, capacity: usize) -> Result<(), RunError> {
    if workers == 0 {
        return Err(RunError::ZeroWorkers);
    }
    if workers > MAX_WORKERS {
        return Err(RunError::TooManyWorkers {
            count: workers,
            limit: MAX_WORKERS,
        });
    }
    if capacity == 0 {
        return Err(RunError::ZeroCapacity);
    }
    if capacity > MAX_CAPACITY {
        return Err(RunError::CapacityTooLarge {
            count: capacity,
            limit: MAX_CAPACITY,
        });
    }
    if tasks.len() > MAX_TASKS {
        return Err(RunError::TooManyTasks {
            count: tasks.len(),
            limit: MAX_TASKS,
        });
    }

    let total_bytes = tasks.iter().try_fold(0_usize, |total, task| {
        total.checked_add(task.text.len())
    });
    let total_bytes = total_bytes.unwrap_or(usize::MAX);
    if total_bytes > MAX_TOTAL_TEXT_BYTES {
        return Err(RunError::TooManyTextBytes {
            count: total_bytes,
            limit: MAX_TOTAL_TEXT_BYTES,
        });
    }

    for (position, task) in tasks.iter().enumerate() {
        if task.index != position {
            return Err(RunError::InvalidTaskIndex {
                position,
                observed: task.index,
            });
        }
    }
    Ok(())
}

fn outcome_index(outcome: &TaskOutcome) -> usize {
    match outcome {
        TaskOutcome::Completed { index, .. }
        | TaskOutcome::Failed { index, .. }
        | TaskOutcome::Panicked { index }
        | TaskOutcome::Cancelled { index } => *index,
    }
}

#[cfg(test)]
mod tests {
    use super::{
        FailurePolicy, RunError, Task, TaskMode, TaskOutcome, MAX_CAPACITY, MAX_WORKERS, run,
    };

    fn task(index: usize, mode: TaskMode) -> Task {
        Task {
            index,
            text: format!("task-{index}"),
            mode,
        }
    }

    #[test]
    fn continue_policy_contains_panic_without_cancelling_later_work() {
        let output = run(
            vec![
                task(0, TaskMode::Normal),
                task(1, TaskMode::DomainFail),
                task(2, TaskMode::Panic),
                task(3, TaskMode::Normal),
            ],
            1,
            1,
            FailurePolicy::Continue,
        )
        .expect("valid configuration");
        assert!(matches!(output[0], TaskOutcome::Completed { index: 0, .. }));
        assert!(matches!(output[1], TaskOutcome::Failed { index: 1, .. }));
        assert!(matches!(output[2], TaskOutcome::Panicked { index: 2 }));
        assert!(matches!(output[3], TaskOutcome::Completed { index: 3, .. }));
    }

    #[test]
    fn fail_fast_keeps_exactly_one_outcome_per_input() {
        let tasks = vec![
            task(0, TaskMode::DomainFail),
            task(1, TaskMode::Spin(100_000)),
            task(2, TaskMode::Normal),
            task(3, TaskMode::Normal),
        ];
        let output = run(tasks, 2, 1, FailurePolicy::FailFast)
            .expect("valid configuration");
        assert_eq!(output.len(), 4);
        for (index, outcome) in output.iter().enumerate() {
            assert_eq!(super::outcome_index(outcome), index);
        }
    }

    #[test]
    fn validates_identity_and_resource_bounds() {
        assert!(matches!(
            run(vec![task(1, TaskMode::Normal)], 1, 1, FailurePolicy::Continue),
            Err(RunError::InvalidTaskIndex { .. })
        ));
        assert!(matches!(
            run(Vec::new(), MAX_WORKERS + 1, 1, FailurePolicy::Continue),
            Err(RunError::TooManyWorkers { .. })
        ));
        assert!(matches!(
            run(Vec::new(), 1, MAX_CAPACITY + 1, FailurePolicy::Continue),
            Err(RunError::CapacityTooLarge { .. })
        ));
    }
}
