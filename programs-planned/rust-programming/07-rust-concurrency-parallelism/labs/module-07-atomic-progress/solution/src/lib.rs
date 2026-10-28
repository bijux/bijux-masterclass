#![forbid(unsafe_code)]

use std::sync::atomic::{AtomicU8, AtomicUsize, Ordering};

#[repr(u8)]
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Phase {
    Created = 0,
    Running = 1,
    Cancelling = 2,
    Finished = 3,
}

impl Phase {
    fn from_u8(value: u8) -> Self {
        match value {
            0 => Self::Created,
            1 => Self::Running,
            2 => Self::Cancelling,
            _ => Self::Finished,
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct LiveSnapshot {
    pub submitted: usize,
    pub finished: usize,
    pub phase: Phase,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct TransitionError {
    pub observed: Phase,
    pub requested: Phase,
}

pub struct AtomicProgress {
    phase: AtomicU8,
    submitted: AtomicUsize,
    finished: AtomicUsize,
    quota: AtomicUsize,
}

impl AtomicProgress {
    #[must_use]
    pub fn new(quota: usize) -> Self {
        Self {
            phase: AtomicU8::new(Phase::Created as u8),
            submitted: AtomicUsize::new(0),
            finished: AtomicUsize::new(0),
            quota: AtomicUsize::new(quota),
        }
    }

    /// Changes only the atomic lifecycle value. It publishes no ordinary data,
    /// so relaxed ordering is sufficient for this deliberately narrow contract.
    pub fn transition(&self, requested: Phase) -> Result<(), TransitionError> {
        let mut observed = Phase::from_u8(self.phase.load(Ordering::Relaxed));
        loop {
            if !legal_transition(observed, requested) {
                return Err(TransitionError {
                    observed,
                    requested,
                });
            }
            match self.phase.compare_exchange_weak(
                observed as u8,
                requested as u8,
                Ordering::Relaxed,
                Ordering::Relaxed,
            ) {
                Ok(_) => return Ok(()),
                Err(actual) => observed = Phase::from_u8(actual),
            }
        }
    }

    pub fn record_submitted(&self) {
        increment_saturating(&self.submitted);
    }

    pub fn record_finished(&self) {
        increment_saturating(&self.finished);
    }

    /// Reserves the entire amount at one linearization point. Reserving zero is
    /// a successful no-op and does not create a scarce-resource claim.
    pub fn reserve(&self, amount: usize) -> bool {
        self.quota
            .fetch_update(Ordering::Relaxed, Ordering::Relaxed, |current| {
                current.checked_sub(amount)
            })
            .is_ok()
    }

    #[must_use]
    pub fn remaining_quota(&self) -> usize {
        self.quota.load(Ordering::Relaxed)
    }

    #[must_use]
    pub fn live(&self) -> LiveSnapshot {
        LiveSnapshot {
            submitted: self.submitted.load(Ordering::Relaxed),
            finished: self.finished.load(Ordering::Relaxed),
            phase: Phase::from_u8(self.phase.load(Ordering::Relaxed)),
        }
    }
}

fn increment_saturating(value: &AtomicUsize) {
    let _ = value.fetch_update(Ordering::Relaxed, Ordering::Relaxed, |current| {
        Some(current.saturating_add(1))
    });
}

#[must_use]
pub const fn legal_transition(from: Phase, to: Phase) -> bool {
    matches!(
        (from, to),
        (Phase::Created, Phase::Running)
            | (Phase::Created, Phase::Cancelling)
            | (Phase::Running, Phase::Cancelling)
            | (Phase::Running, Phase::Finished)
            | (Phase::Cancelling, Phase::Finished)
    )
}

/// A one-writer-wins publication slot.
///
/// State `0` is empty, `1` is claimed by a publisher, and `2` is ready. The
/// release store to `2` publishes the preceding value store. A reader that
/// observes `2` with acquire ordering may then read the value.
pub struct PublishedUsize {
    state: AtomicU8,
    value: AtomicUsize,
}

impl Default for PublishedUsize {
    fn default() -> Self {
        Self::new()
    }
}

impl PublishedUsize {
    #[must_use]
    pub const fn new() -> Self {
        Self {
            state: AtomicU8::new(0),
            value: AtomicUsize::new(0),
        }
    }

    pub fn try_publish(&self, value: usize) -> Result<(), usize> {
        if self
            .state
            .compare_exchange(0, 1, Ordering::Relaxed, Ordering::Relaxed)
            .is_err()
        {
            return Err(value);
        }
        self.value.store(value, Ordering::Relaxed);
        self.state.store(2, Ordering::Release);
        Ok(())
    }

    #[must_use]
    pub fn load(&self) -> Option<usize> {
        if self.state.load(Ordering::Acquire) == 2 {
            Some(self.value.load(Ordering::Relaxed))
        } else {
            None
        }
    }
}

#[cfg(test)]
mod tests {
    use super::{AtomicProgress, Phase, PublishedUsize};
    use std::sync::{Arc, Barrier};
    use std::thread;

    #[test]
    fn one_competing_start_wins() {
        let progress = Arc::new(AtomicProgress::new(10));
        let gate = Arc::new(Barrier::new(3));
        let handles: Vec<_> = (0..2)
            .map(|_| {
                let progress = Arc::clone(&progress);
                let gate = Arc::clone(&gate);
                thread::spawn(move || {
                    gate.wait();
                    progress.transition(Phase::Running)
                })
            })
            .collect();
        gate.wait();
        assert_eq!(
            handles
                .into_iter()
                .filter(|handle| handle.join().expect("worker joins").is_ok())
                .count(),
            1
        );
    }

    #[test]
    fn quota_reservation_is_one_transition() {
        let progress = Arc::new(AtomicProgress::new(1));
        let handles: Vec<_> = (0..2)
            .map(|_| {
                let progress = Arc::clone(&progress);
                thread::spawn(move || progress.reserve(1))
            })
            .collect();
        assert_eq!(
            handles
                .into_iter()
                .filter(|handle| handle.join().expect("worker joins"))
                .count(),
            1
        );
        assert_eq!(progress.remaining_quota(), 0);
    }

    #[test]
    fn live_metrics_are_independent_observations() {
        let progress = AtomicProgress::new(0);
        progress.record_finished();
        let snapshot = progress.live();
        assert_eq!(snapshot.finished, 1);
        assert_eq!(
            snapshot.submitted, 0,
            "the API does not promise a coherent multi-counter relation"
        );
    }

    #[test]
    fn release_acquire_publishes_the_value() {
        let slot = Arc::new(PublishedUsize::new());
        let writer = {
            let slot = Arc::clone(&slot);
            thread::spawn(move || slot.try_publish(41))
        };
        assert_eq!(writer.join().expect("writer joins"), Ok(()));
        assert_eq!(slot.load(), Some(41));
        assert_eq!(slot.try_publish(99), Err(99));
        assert_eq!(slot.load(), Some(41));
    }
}
