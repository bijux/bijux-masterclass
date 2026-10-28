//! Compiling vocabulary for the service-desk policy laboratory.
//!
//! The learner derives and implements `decision_reason` from the truth table.

/// Accepted decision reason.
pub const ACCEPTED: &str = "accepted";
/// Invalid weekday reason.
pub const INVALID_WEEKDAY: &str = "invalid-weekday";
/// Invalid hour reason.
pub const INVALID_HOUR: &str = "invalid-hour";
/// Invalid duration reason.
pub const INVALID_DURATION: &str = "invalid-duration";
/// Outside service hours reason.
pub const OUTSIDE_SERVICE_HOURS: &str = "outside-service-hours";
/// Duration limit reason.
pub const DURATION_EXCEEDED: &str = "duration-exceeded";
/// Queue limit reason.
pub const QUEUE_CAPACITY_REACHED: &str = "queue-capacity-reached";

/// Reports whether a returned reason represents acceptance.
pub fn is_accepted(reason: &str) -> bool {
    reason == ACCEPTED
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn stable_reason_vocabulary_is_exact() {
        assert!(is_accepted(ACCEPTED));
        assert!(!is_accepted("Accepted"));
        assert_ne!(INVALID_WEEKDAY, INVALID_HOUR);
        assert_ne!(DURATION_EXCEEDED, QUEUE_CAPACITY_REACHED);
    }
}
