#![forbid(unsafe_code)]

#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)]
pub struct Metrics {
    pub count: usize,
    pub total: i64,
    pub minimum: Option<i64>,
    pub maximum: Option<i64>,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum MetricError {
    Overflow,
}

#[cfg(test)]
mod tests {
    use super::Metrics;

    #[test]
    fn empty_metrics_have_no_extrema() {
        let metrics = Metrics::default();
        assert_eq!(metrics.count, 0);
        assert_eq!(metrics.minimum, None);
        assert_eq!(metrics.maximum, None);
    }
}
