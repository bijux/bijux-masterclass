#![forbid(unsafe_code)]

#[repr(u8)]
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Phase { Created = 0, Running = 1, Cancelling = 2, Finished = 3 }

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct LiveSnapshot { pub submitted: usize, pub finished: usize, pub phase: Phase }

#[must_use]
pub const fn legal_transition(from: Phase, to: Phase) -> bool {
    matches!((from, to),
        (Phase::Created, Phase::Running)
        | (Phase::Created, Phase::Cancelling)
        | (Phase::Running, Phase::Cancelling)
        | (Phase::Running, Phase::Finished)
        | (Phase::Cancelling, Phase::Finished))
}

#[cfg(test)]
mod tests {
    use super::{Phase, legal_transition};
    #[test]
    fn baseline_transition_table_is_explicit() {
        assert!(legal_transition(Phase::Running, Phase::Finished));
        assert!(!legal_transition(Phase::Finished, Phase::Running));
    }
}
