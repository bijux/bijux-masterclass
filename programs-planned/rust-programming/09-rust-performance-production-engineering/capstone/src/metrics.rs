use std::sync::atomic::{AtomicU64, AtomicUsize, Ordering};

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct MetricsSnapshot {
    pub accepted_records: u64,
    pub rejected_invalid: u64,
    pub rejected_overloaded: u64,
    pub completed_snapshots: u64,
    pub active_connections_observed: usize,
    pub queue_depth_observed: usize,
}

#[derive(Debug, Default)]
pub struct Metrics {
    accepted_records: AtomicU64,
    rejected_invalid: AtomicU64,
    rejected_overloaded: AtomicU64,
    completed_snapshots: AtomicU64,
    active_connections: AtomicUsize,
    queue_depth: AtomicUsize,
}

impl Metrics {
    pub fn accepted(&self) {
        self.accepted_records.fetch_add(1, Ordering::Relaxed);
    }

    pub fn invalid(&self) {
        self.rejected_invalid.fetch_add(1, Ordering::Relaxed);
    }

    pub fn overloaded(&self) {
        self.rejected_overloaded.fetch_add(1, Ordering::Relaxed);
    }

    pub fn snapshot_completed(&self) {
        self.completed_snapshots.fetch_add(1, Ordering::Relaxed);
    }

    pub fn connection_opened(&self) {
        self.active_connections.fetch_add(1, Ordering::Relaxed);
    }

    pub fn connection_closed(&self) {
        self.active_connections.fetch_sub(1, Ordering::Relaxed);
    }

    pub fn set_queue_depth(&self, value: usize) {
        self.queue_depth.store(value, Ordering::Relaxed);
    }

    pub fn snapshot(&self) -> MetricsSnapshot {
        MetricsSnapshot {
            accepted_records: self.accepted_records.load(Ordering::Relaxed),
            rejected_invalid: self.rejected_invalid.load(Ordering::Relaxed),
            rejected_overloaded: self.rejected_overloaded.load(Ordering::Relaxed),
            completed_snapshots: self.completed_snapshots.load(Ordering::Relaxed),
            active_connections_observed: self.active_connections.load(Ordering::Relaxed),
            queue_depth_observed: self.queue_depth.load(Ordering::Relaxed),
        }
    }
}
