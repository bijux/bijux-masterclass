#![forbid(unsafe_code)]

pub const MAX_ITEMS: usize = 1024;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum MapOutcome { Squared(i64), Overflow }

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum PipelineError {
    ZeroWorkers,
    TooManyItems { count: usize, limit: usize },
}

#[must_use]
pub fn square(value: i64) -> MapOutcome {
    value.checked_mul(value).map_or(MapOutcome::Overflow, MapOutcome::Squared)
}

#[cfg(test)]
mod tests {
    use super::{MapOutcome, square};
    #[test]
    fn baseline_square_is_typed() {
        assert_eq!(square(4), MapOutcome::Squared(16));
        assert_eq!(square(i64::MAX), MapOutcome::Overflow);
    }
}
