#![forbid(unsafe_code)]

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Snapshot {
    pub capacity: u64,
    pub available: u64,
    pub reserved: u64,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum InventoryError {
    Insufficient { requested: u64, available: u64 },
    InvalidRelease { requested: u64, reserved: u64 },
    Interrupted,
}

impl Snapshot {
    #[must_use]
    pub fn invariant_holds(self) -> bool {
        self.available <= self.capacity
            && self.reserved <= self.capacity
            && self.available.checked_add(self.reserved) == Some(self.capacity)
    }
}

#[cfg(test)]
mod tests {
    use super::Snapshot;
    #[test]
    fn baseline_invariant_is_explicit() {
        assert!(Snapshot { capacity: 10, available: 7, reserved: 3 }.invariant_holds());
        assert!(!Snapshot { capacity: 10, available: 7, reserved: 4 }.invariant_holds());
    }
}
