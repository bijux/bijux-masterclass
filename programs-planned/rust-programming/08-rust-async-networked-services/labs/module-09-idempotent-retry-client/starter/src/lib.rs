//! Starter surface for the idempotent retry laboratory.
//!
//! The starter makes retry policy and failure classes explicit. You still
//! need to build the server-side idempotency state machine, scripted ambiguous
//! failures, one-deadline retry loop, deterministic jitter, and execution-count
//! proof.

use std::time::Duration;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct RetryPolicy {
    pub max_attempts: u32,
    pub initial_delay: Duration,
    pub max_delay: Duration,
    pub overall_deadline: Duration,
}

impl RetryPolicy {
    pub fn validate(self) -> Result<Self, &'static str> {
        if self.max_attempts == 0 {
            return Err("max_attempts must be nonzero");
        }
        if self.initial_delay.is_zero() || self.max_delay.is_zero() {
            return Err("retry delays must be nonzero");
        }
        if self.initial_delay > self.max_delay {
            return Err("initial_delay cannot exceed max_delay");
        }
        if self.overall_deadline.is_zero() {
            return Err("overall_deadline must be nonzero");
        }
        Ok(self)
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Failure {
    Busy { retry_after: Option<Duration> },
    Transport,
    Conflict,
    Capacity,
    Domain(String),
}

impl Failure {
    pub fn is_retryable(&self) -> bool {
        matches!(self, Self::Busy { .. } | Self::Transport)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn retry_policy_rejects_an_inverted_delay_range() {
        let result = RetryPolicy {
            max_attempts: 3,
            initial_delay: Duration::from_secs(2),
            max_delay: Duration::from_secs(1),
            overall_deadline: Duration::from_secs(10),
        }
        .validate();
        assert!(result.is_err());
    }

    #[test]
    fn domain_failure_is_not_retryable() {
        assert!(!Failure::Domain("invalid request".to_owned()).is_retryable());
    }
}
