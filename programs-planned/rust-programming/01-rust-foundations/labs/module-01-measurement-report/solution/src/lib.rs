//! Reference implementation for the fixed-size measurement report.

/// Number of readings in one report.
pub const SAMPLE_COUNT: usize = 5;

/// Computes minimum, maximum, and a widened total in one pass.
pub fn summarize(values: [i32; SAMPLE_COUNT]) -> (i32, i32, i64) {
    let mut minimum = values[0];
    let mut maximum = values[0];
    let mut total = 0_i64;

    for value in values {
        minimum = minimum.min(value);
        maximum = maximum.max(value);
        total += i64::from(value);
    }

    (minimum, maximum, total)
}

/// Computes the arithmetic mean for the fixed sample count.
pub fn mean(total: i64) -> f64 {
    total as f64 / SAMPLE_COUNT as f64
}

/// Counts readings strictly below `threshold`.
pub fn count_below(values: [i32; SAMPLE_COUNT], threshold: i32) -> usize {
    values.into_iter().filter(|value| *value < threshold).count()
}

/// Renders the deterministic report used by the binary and tests.
pub fn render(values: [i32; SAMPLE_COUNT]) -> String {
    let (minimum, maximum, total) = summarize(values);
    let readings = values.map(|value| value.to_string()).join(" ");
    format!(
        concat!(
            "readings: {readings}\n",
            "minimum: {minimum}\n",
            "maximum: {maximum}\n",
            "total: {total}\n",
            "mean: {:.2}\n",
            "below_freezing: {}",
        ),
        mean(total),
        count_below(values, 0),
    )
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn sample_contract_is_exact() {
        let values = [12, -4, 18, 0, 11];
        assert_eq!(summarize(values), (-4, 18, 37));
        assert_eq!(count_below(values, 0), 1);
        assert_eq!(mean(37), 7.4);
    }

    #[test]
    fn all_negative_values_preserve_real_maximum() {
        assert_eq!(summarize([-9, -2, -7, -3, -8]), (-9, -2, -29));
    }

    #[test]
    fn all_equal_values_have_equal_extrema() {
        assert_eq!(summarize([4; SAMPLE_COUNT]), (4, 4, 20));
    }

    #[test]
    fn threshold_is_exclusive() {
        assert_eq!(count_below([-1, 0, 1, 0, -2], 0), 2);
    }

    #[test]
    fn widened_total_handles_integer_extremes() {
        let values = [i32::MAX, i32::MAX, i32::MIN, i32::MIN, 0];
        assert_eq!(summarize(values), (i32::MIN, i32::MAX, -2));
    }

    #[test]
    fn rendering_is_stable_and_preserves_order() {
        assert_eq!(
            render([12, -4, 18, 0, 11]),
            concat!(
                "readings: 12 -4 18 0 11\n",
                "minimum: -4\n",
                "maximum: 18\n",
                "total: 37\n",
                "mean: 7.40\n",
                "below_freezing: 1",
            ),
        );
    }
}
