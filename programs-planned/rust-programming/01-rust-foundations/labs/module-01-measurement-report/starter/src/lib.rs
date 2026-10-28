//! Compiling baseline for the measurement-report laboratory.
//!
//! The required summary and rendering API belongs to the learner. This crate
//! supplies only the fixed-size input vocabulary and an order-preserving helper.

/// Number of readings in one device sample.
pub const SAMPLE_COUNT: usize = 5;

/// Formats only the input row, preserving the original array order.
pub fn readings_line(values: &[i32; SAMPLE_COUNT]) -> String {
    let body = values
        .iter()
        .map(|value| value.to_string())
        .collect::<Vec<_>>()
        .join(" ");
    format!("readings: {body}")
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn baseline_formatter_preserves_order() {
        let values = [12, -4, 18, 0, 11];
        assert_eq!(readings_line(&values), "readings: 12 -4 18 0 11");
        assert_eq!(values, [12, -4, 18, 0, 11]);
    }
}
