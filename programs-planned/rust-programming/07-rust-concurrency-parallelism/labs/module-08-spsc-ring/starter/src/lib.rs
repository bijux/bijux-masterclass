#![deny(unsafe_op_in_unsafe_fn)]

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum RingError { ZeroCapacity, CapacityOverflow }

#[derive(Debug, PartialEq, Eq)]
pub struct Full<T>(pub T);

#[must_use]
pub fn physical_slots(capacity: usize) -> Result<usize, RingError> {
    if capacity == 0 { return Err(RingError::ZeroCapacity); }
    capacity.checked_add(1).ok_or(RingError::CapacityOverflow)
}

#[cfg(test)]
mod tests {
    use super::{RingError, physical_slots};
    #[test]
    fn baseline_sentinel_slot_is_explicit() {
        assert_eq!(physical_slots(1), Ok(2));
        assert_eq!(physical_slots(0), Err(RingError::ZeroCapacity));
    }
}
