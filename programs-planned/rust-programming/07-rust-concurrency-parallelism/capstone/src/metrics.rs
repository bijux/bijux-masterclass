use std::sync::atomic::{AtomicUsize, Ordering};

#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)]
pub struct MetricsSnapshot {
    pub submitted: usize,
    pub started: usize,
    pub completed: usize,
    pub failed: usize,
    pub panicked: usize,
    pub cancelled: usize,
}

#[derive(Debug, Default)]
pub(crate) struct Metrics {
    submitted: AtomicUsize,
    started: AtomicUsize,
    completed: AtomicUsize,
    failed: AtomicUsize,
    panicked: AtomicUsize,
    cancelled: AtomicUsize,
}

fn increment(counter: &AtomicUsize) {
    let _ = counter.fetch_update(Ordering::Relaxed, Ordering::Relaxed, |current| {
        Some(current.saturating_add(1))
    });
}

impl Metrics {
    pub(crate) fn submitted(&self) { increment(&self.submitted); }
    pub(crate) fn started(&self) { increment(&self.started); }
    pub(crate) fn completed(&self) { increment(&self.completed); }
    pub(crate) fn failed(&self) { increment(&self.failed); }
    pub(crate) fn panicked(&self) { increment(&self.panicked); }
    pub(crate) fn cancelled(&self) { increment(&self.cancelled); }

    pub(crate) fn snapshot(&self) -> MetricsSnapshot {
        MetricsSnapshot {
            submitted: self.submitted.load(Ordering::Relaxed),
            started: self.started.load(Ordering::Relaxed),
            completed: self.completed.load(Ordering::Relaxed),
            failed: self.failed.load(Ordering::Relaxed),
            panicked: self.panicked.load(Ordering::Relaxed),
            cancelled: self.cancelled.load(Ordering::Relaxed),
        }
    }
}
