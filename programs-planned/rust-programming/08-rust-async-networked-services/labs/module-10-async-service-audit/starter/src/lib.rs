//! Starter surface for the final async-service audit laboratory.
//!
//! The starter defines a complete resource envelope and terminal vocabulary.
//! You still need to build the actor, idempotency records, bounded duplicate
//! waiters, active delivery set, status snapshots, graceful shutdown, fault
//! injection, and architecture dossier.

use std::time::Duration;

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
    pub fn validate(self) -> Result<Self, &'static str> {
        if !(1..=16).contains(&self.mailbox) {
            return Err("mailbox must be in 1..=16");
        }
        if !(1..=16).contains(&self.pending) {
            return Err("pending must be in 1..=16");
        }
        if !(1..=4).contains(&self.active) {
            return Err("active must be in 1..=4");
        }
        if !(1..=64).contains(&self.records) {
            return Err("records must be in 1..=64");
        }
        if !(1..=8).contains(&self.waiters_per_key) {
            return Err("waiters_per_key must be in 1..=8");
        }
        if self.shutdown_grace.is_zero() {
            return Err("shutdown_grace must be nonzero");
        }
        Ok(self)
    }
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

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn final_lab_names_every_bounded_location() {
        assert!(
            Limits {
                mailbox: 8,
                pending: 16,
                active: 4,
                records: 64,
                waiters_per_key: 8,
                shutdown_grace: Duration::from_secs(2),
            }
            .validate()
            .is_ok()
        );
    }
}
