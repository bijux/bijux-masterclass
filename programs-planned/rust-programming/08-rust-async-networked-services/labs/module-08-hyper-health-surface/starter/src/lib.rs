//! Starter surface for the Hyper health-surface laboratory.
//!
//! The starter defines operational state, a stable text representation, and
//! explicit server limits. You still need to build the actual listener,
//! per-connection service, body bound, method/path policy, connection
//! supervision, and graceful shutdown.

use std::time::Duration;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Health {
    Starting,
    Ready,
    ShuttingDown,
    Failed,
}

impl Health {
    pub fn as_str(self) -> &'static str {
        match self {
            Self::Starting => "starting",
            Self::Ready => "ready",
            Self::ShuttingDown => "shutting-down",
            Self::Failed => "failed",
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Snapshot {
    pub health: Health,
    pub active: usize,
    pub queued: usize,
}

#[derive(Debug, Clone, Copy)]
pub struct HttpLimits {
    pub max_connections: usize,
    pub max_body_bytes: usize,
    pub shutdown_grace: Duration,
}

pub fn render(snapshot: &Snapshot) -> String {
    format!(
        "state={}\nactive={}\nqueued={}\n",
        snapshot.health.as_str(),
        snapshot.active,
        snapshot.queued
    )
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn rendering_is_stable_and_not_debug_derived() {
        let text = render(&Snapshot {
            health: Health::Ready,
            active: 1,
            queued: 2,
        });
        assert_eq!(text, "state=ready\nactive=1\nqueued=2\n");
    }
}
