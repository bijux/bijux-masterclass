//! Compiling boundary vocabulary for the ownership-intake laboratory.
//!
//! Normalization and ownership transfer remain the learner's work.

/// Maximum accepted normalized title length in UTF-8 bytes.
pub const MAX_TITLE_BYTES: usize = 80;

/// Classifies an already-normalized title according to the storage boundary.
///
/// This helper deliberately does not normalize or take ownership.
pub fn normalized_is_accepted(value: &str) -> bool {
    !value.is_empty() && value.len() <= MAX_TITLE_BYTES
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn baseline_policy_is_byte_based() {
        assert!(normalized_is_accepted(&"é".repeat(40)));
        assert!(!normalized_is_accepted(&"é".repeat(41)));
        assert!(!normalized_is_accepted(""));
    }
}
