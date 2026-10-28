//! Reference implementation for the service-desk control-flow policy.

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

/// Returns a stable reason code for one appointment request.
pub const fn decision_reason(
    weekday: u8,
    hour: u8,
    minutes: u16,
    queue_length: u16,
    urgent: bool,
) -> &'static str {
    if weekday < 1 || weekday > 7 {
        return INVALID_WEEKDAY;
    }
    if hour > 23 {
        return INVALID_HOUR;
    }
    if minutes == 0 {
        return INVALID_DURATION;
    }

    if urgent {
        if hour < 7 || hour > 21 {
            return OUTSIDE_SERVICE_HOURS;
        }
        if minutes > 120 {
            return DURATION_EXCEEDED;
        }
        if queue_length >= 20 {
            return QUEUE_CAPACITY_REACHED;
        }
    } else {
        if weekday > 5 || hour < 9 || hour > 16 {
            return OUTSIDE_SERVICE_HOURS;
        }
        if minutes > 60 {
            return DURATION_EXCEEDED;
        }
        if queue_length >= 8 {
            return QUEUE_CAPACITY_REACHED;
        }
    }

    ACCEPTED
}

/// Reports whether a returned reason represents acceptance.
pub fn is_accepted(reason: &str) -> bool {
    reason == ACCEPTED
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn malformed_inputs_precede_policy() {
        assert_eq!(decision_reason(0, 30, 0, 100, false), INVALID_WEEKDAY);
        assert_eq!(decision_reason(1, 24, 0, 100, false), INVALID_HOUR);
        assert_eq!(decision_reason(1, 9, 0, 100, false), INVALID_DURATION);
    }

    #[test]
    fn ordinary_hour_boundaries_are_exact() {
        assert_eq!(decision_reason(1, 8, 30, 0, false), OUTSIDE_SERVICE_HOURS);
        assert_eq!(decision_reason(1, 9, 30, 0, false), ACCEPTED);
        assert_eq!(decision_reason(5, 16, 30, 0, false), ACCEPTED);
        assert_eq!(decision_reason(5, 17, 30, 0, false), OUTSIDE_SERVICE_HOURS);
        assert_eq!(decision_reason(6, 12, 30, 0, false), OUTSIDE_SERVICE_HOURS);
    }

    #[test]
    fn ordinary_duration_and_queue_boundaries_are_exact() {
        assert_eq!(decision_reason(3, 12, 60, 7, false), ACCEPTED);
        assert_eq!(decision_reason(3, 12, 61, 7, false), DURATION_EXCEEDED);
        assert_eq!(decision_reason(3, 12, 60, 8, false), QUEUE_CAPACITY_REACHED);
    }

    #[test]
    fn urgent_boundaries_are_exact() {
        assert_eq!(decision_reason(7, 6, 30, 0, true), OUTSIDE_SERVICE_HOURS);
        assert_eq!(decision_reason(7, 7, 120, 19, true), ACCEPTED);
        assert_eq!(decision_reason(7, 21, 120, 19, true), ACCEPTED);
        assert_eq!(decision_reason(7, 22, 120, 19, true), OUTSIDE_SERVICE_HOURS);
        assert_eq!(decision_reason(7, 12, 121, 19, true), DURATION_EXCEEDED);
        assert_eq!(decision_reason(7, 12, 120, 20, true), QUEUE_CAPACITY_REACHED);
    }

    #[test]
    fn urgent_and_ordinary_truth_table_differs_only_by_policy() {
        let cases = [
            (7, 8, 90, 10, false, OUTSIDE_SERVICE_HOURS),
            (7, 8, 90, 10, true, ACCEPTED),
            (3, 12, 90, 10, false, DURATION_EXCEEDED),
            (3, 12, 90, 10, true, ACCEPTED),
        ];
        for (weekday, hour, minutes, queue, urgent, expected) in cases {
            assert_eq!(decision_reason(weekday, hour, minutes, queue, urgent), expected);
        }
    }

    #[test]
    fn accepted_helper_does_not_accept_unknown_text() {
        assert!(is_accepted(ACCEPTED));
        assert!(!is_accepted("Accepted"));
        assert!(!is_accepted("unknown"));
    }
}
