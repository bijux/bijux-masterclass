//! Starter surface for the bounded relay broker laboratory.
//!
//! The starter defines the externally visible limits and outcomes. The actor,
//! queue, task set, snapshots, commitment point, shutdown protocol, and tests
//! remain for you to design.

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Limits {
    pub mailbox: usize,
    pub queued: usize,
    pub active: usize,
}

impl Limits {
    pub fn validate(self) -> Result<Self, &'static str> {
        if self.mailbox == 0 {
            return Err("mailbox capacity must be nonzero");
        }
        if self.queued == 0 {
            return Err("waiting-queue capacity must be nonzero");
        }
        if self.active == 0 {
            return Err("active-job capacity must be nonzero");
        }
        Ok(self)
    }
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

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn every_capacity_is_explicit() {
        assert!(
            Limits {
                mailbox: 4,
                queued: 2,
                active: 1,
            }
            .validate()
            .is_ok()
        );
        assert!(
            Limits {
                mailbox: 1,
                queued: 0,
                active: 1,
            }
            .validate()
            .is_err()
        );
    }
}
