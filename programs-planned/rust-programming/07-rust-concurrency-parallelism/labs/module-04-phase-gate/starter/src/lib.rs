#![forbid(unsafe_code)]

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum Phase { Created, Prepared, Running, Finished }

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum WaitResult { Reached(Phase), Cancelled, TimedOut(Phase) }

#[must_use]
pub const fn next_phase(phase: Phase) -> Option<Phase> {
    match phase {
        Phase::Created => Some(Phase::Prepared),
        Phase::Prepared => Some(Phase::Running),
        Phase::Running => Some(Phase::Finished),
        Phase::Finished => None,
    }
}

#[cfg(test)]
mod tests {
    use super::{Phase, next_phase};
    #[test]
    fn baseline_phase_order_is_explicit() {
        assert_eq!(next_phase(Phase::Prepared), Some(Phase::Running));
        assert_eq!(next_phase(Phase::Finished), None);
    }
}
