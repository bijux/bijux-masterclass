//! Identity baseline for the typed workflow-state laboratory.
//!
//! The lifecycle states, transition commands, document representation, and
//! exhaustive transition table remain the learner's work.

use std::fmt;

/// Stable nonzero document identity.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, PartialOrd, Ord)]
pub struct DocumentId(u64);

impl DocumentId {
    /// Constructs an identifier when `value` is nonzero.
    pub const fn new(value: u64) -> Option<Self> {
        if value == 0 {
            None
        } else {
            Some(Self(value))
        }
    }

    /// Returns the primitive identifier value.
    pub const fn get(self) -> u64 {
        self.0
    }
}

impl fmt::Display for DocumentId {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        self.0.fmt(formatter)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn baseline_identity_rejects_zero() {
        assert_eq!(DocumentId::new(0), None);
        let id = DocumentId::new(7).expect("seven is nonzero");
        assert_eq!(id.get(), 7);
        assert_eq!(id.to_string(), "7");
    }
}
