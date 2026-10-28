//! Tokenization and domain-vocabulary baseline for the record-codec laboratory.
//!
//! Semantic conversion, aggregate validation, contextual errors, and buffered
//! I/O remain the learner's work.

use std::fmt;

/// Supported storage version marker.
pub const HEADER: &str = "INVENTORY-V1";
/// Maximum title size in UTF-8 bytes.
pub const MAX_TITLE_BYTES: usize = 120;

/// Nonzero item identity.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, PartialOrd, Ord)]
pub struct ItemId(u64);

impl ItemId {
    /// Constructs a nonzero identity.
    pub const fn new(value: u64) -> Option<Self> {
        if value == 0 {
            None
        } else {
            Some(Self(value))
        }
    }

    /// Returns the primitive identity value.
    pub const fn get(self) -> u64 {
        self.0
    }
}

impl fmt::Display for ItemId {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        self.0.fmt(formatter)
    }
}

/// Persisted item-state vocabulary. Parsing remains part of the lab.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ItemState {
    /// Item can be checked out.
    Available,
    /// Item is currently checked out.
    CheckedOut,
}

/// Splits an item line without converting or validating fields.
pub fn split_item_fields(line: &str) -> Vec<&str> {
    line.split('\t').collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn baseline_tokenization_does_not_claim_validation() {
        assert_eq!(HEADER, "INVENTORY-V1");
        assert_eq!(ItemId::new(0), None);
        assert_eq!(split_item_fields("ITEM\t7\tavailable\tRust"), ["ITEM", "7", "available", "Rust"]);
        assert_eq!(split_item_fields("ITEM\tbad"), ["ITEM", "bad"]);
    }
}
