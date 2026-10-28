#![forbid(unsafe_code)]

use std::sync::{Arc, Barrier, Condvar, Mutex};
use std::thread;
use std::time::{Duration, Instant};

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum Phase {
    Created,
    Prepared,
    Running,
    Finished,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum WaitResult {
    Reached(Phase),
    Cancelled,
    TimedOut(Phase),
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum TransitionError {
    Cancelled,
    Finished,
    NotNext { current: Phase, requested: Phase },
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum CohortError {
    WorkerPanicked { participant: usize },
    SumOverflow,
}

#[derive(Debug, Clone, Copy)]
struct State {
    phase: Phase,
    cancelled: bool,
}

pub struct PhaseGate {
    state: Mutex<State>,
    changed: Condvar,
}

impl Default for PhaseGate {
    fn default() -> Self {
        Self::new()
    }
}

impl PhaseGate {
    #[must_use]
    pub fn new() -> Self {
        Self {
            state: Mutex::new(State {
                phase: Phase::Created,
                cancelled: false,
            }),
            changed: Condvar::new(),
        }
    }

    pub fn advance(&self, requested: Phase) -> Result<Phase, TransitionError> {
        let mut state = self.state.lock().unwrap_or_else(|poison| poison.into_inner());
        if state.cancelled {
            return Err(TransitionError::Cancelled);
        }
        if state.phase == requested {
            return Ok(state.phase);
        }
        if state.phase == Phase::Finished {
            return Err(TransitionError::Finished);
        }
        if next_phase(state.phase) != Some(requested) {
            return Err(TransitionError::NotNext {
                current: state.phase,
                requested,
            });
        }

        state.phase = requested;
        let phase = state.phase;
        drop(state);
        self.changed.notify_all();
        Ok(phase)
    }

    pub fn cancel(&self) {
        let mut state = self.state.lock().unwrap_or_else(|poison| poison.into_inner());
        state.cancelled = true;
        drop(state);
        self.changed.notify_all();
    }

    #[must_use]
    pub fn wait_until(&self, target: Phase) -> WaitResult {
        let mut state = self.state.lock().unwrap_or_else(|poison| poison.into_inner());
        while !state.cancelled && state.phase < target {
            state = self
                .changed
                .wait(state)
                .unwrap_or_else(|poison| poison.into_inner());
        }
        if state.cancelled {
            WaitResult::Cancelled
        } else {
            WaitResult::Reached(state.phase)
        }
    }

    #[must_use]
    pub fn wait_until_timeout(&self, target: Phase, timeout: Duration) -> WaitResult {
        let deadline = Instant::now().checked_add(timeout);
        let mut state = self.state.lock().unwrap_or_else(|poison| poison.into_inner());

        while !state.cancelled && state.phase < target {
            if let Some(deadline) = deadline {
                let now = Instant::now();
                if now >= deadline {
                    return WaitResult::TimedOut(state.phase);
                }
                let remaining = deadline.saturating_duration_since(now);
                let (next, _) = self
                    .changed
                    .wait_timeout(state, remaining)
                    .unwrap_or_else(|poison| poison.into_inner());
                state = next;
            } else {
                // An unrepresentably distant deadline is effectively unbounded.
                state = self
                    .changed
                    .wait(state)
                    .unwrap_or_else(|poison| poison.into_inner());
            }
        }

        if state.cancelled {
            WaitResult::Cancelled
        } else {
            WaitResult::Reached(state.phase)
        }
    }

    pub fn poke(&self) {
        self.changed.notify_all();
    }
}

#[must_use]
pub const fn next_phase(phase: Phase) -> Option<Phase> {
    match phase {
        Phase::Created => Some(Phase::Prepared),
        Phase::Prepared => Some(Phase::Running),
        Phase::Running => Some(Phase::Finished),
        Phase::Finished => None,
    }
}

pub fn fixed_cohort_sum(values: Vec<i64>) -> Result<i64, CohortError> {
    if values.is_empty() {
        return Ok(0);
    }

    let barrier = Arc::new(Barrier::new(values.len()));
    let handles: Vec<_> = values
        .into_iter()
        .enumerate()
        .map(|(participant, value)| {
            let barrier = Arc::clone(&barrier);
            (participant, thread::spawn(move || {
                barrier.wait();
                value
            }))
        })
        .collect();

    let mut total = 0_i64;
    let mut first_panic = None;
    let mut overflowed = false;
    for (participant, handle) in handles {
        match handle.join() {
            Ok(value) => match total.checked_add(value) {
                Some(next) => total = next,
                None => overflowed = true,
            },
            Err(_) if first_panic.is_none() => {
                first_panic = Some(CohortError::WorkerPanicked { participant });
            }
            Err(_) => {}
        }
    }

    if let Some(error) = first_panic {
        Err(error)
    } else if overflowed {
        Err(CohortError::SumOverflow)
    } else {
        Ok(total)
    }
}

#[cfg(test)]
mod tests {
    use super::{
        CohortError, Phase, PhaseGate, TransitionError, WaitResult, fixed_cohort_sum,
    };
    use std::sync::{Arc, mpsc};
    use std::thread;
    use std::time::Duration;

    #[test]
    fn waiters_follow_state_not_notification_history() {
        let gate = PhaseGate::new();
        gate.advance(Phase::Prepared).expect("legal transition");
        gate.poke();
        assert_eq!(
            gate.wait_until(Phase::Prepared),
            WaitResult::Reached(Phase::Prepared)
        );
    }

    #[test]
    fn cancellation_releases_waiter() {
        let gate = Arc::new(PhaseGate::new());
        let (ready_tx, ready_rx) = mpsc::channel();
        let child = {
            let gate = Arc::clone(&gate);
            thread::spawn(move || {
                ready_tx.send(()).expect("receiver remains alive");
                gate.wait_until(Phase::Finished)
            })
        };
        ready_rx.recv().expect("child reached wait boundary");
        gate.cancel();
        assert_eq!(child.join().expect("child joins"), WaitResult::Cancelled);
    }

    #[test]
    fn rejects_skipped_phase_and_respects_one_deadline() {
        let gate = PhaseGate::new();
        assert!(matches!(
            gate.advance(Phase::Running),
            Err(TransitionError::NotNext { .. })
        ));
        assert!(matches!(
            gate.wait_until_timeout(Phase::Running, Duration::ZERO),
            WaitResult::TimedOut(Phase::Created)
        ));
    }

    #[test]
    fn fixed_cohort_joins_every_participant_and_checks_the_sum() {
        assert_eq!(fixed_cohort_sum(vec![1, 2, 3]), Ok(6));
        assert_eq!(
            fixed_cohort_sum(vec![i64::MAX, 1]),
            Err(CohortError::SumOverflow)
        );
    }
}
