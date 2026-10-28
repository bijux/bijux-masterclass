#![forbid(unsafe_code)]

use std::ops::ControlFlow;

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

impl Metrics {
    fn observe(mut self, value: i64) -> Result<Self, MetricError> {
        self.count += 1;
        self.total = self
            .total
            .checked_add(value)
            .ok_or(MetricError::Overflow)?;
        self.minimum = Some(self.minimum.map_or(value, |current| current.min(value)));
        self.maximum = Some(self.maximum.map_or(value, |current| current.max(value)));
        Ok(self)
    }
}

pub fn summarize<I>(values: I) -> Result<Metrics, MetricError>
where
    I: IntoIterator<Item = i64>,
{
    values
        .into_iter()
        .try_fold(Metrics::default(), Metrics::observe)
}

pub fn running_totals<I>(values: I) -> impl Iterator<Item = Result<i64, MetricError>>
where
    I: IntoIterator<Item = i64>,
{
    values.into_iter().scan(Some(0_i64), |state, value| {
        let current = (*state)?;
        match current.checked_add(value) {
            Some(next) => {
                *state = Some(next);
                Some(Ok(next))
            }
            None => {
                *state = None;
                Some(Err(MetricError::Overflow))
            }
        }
    })
}

pub fn first_prefix_over<I>(
    values: I,
    limit: i64,
) -> Result<Option<(usize, i64)>, MetricError>
where
    I: IntoIterator<Item = i64>,
{
    let outcome = values
        .into_iter()
        .enumerate()
        .try_fold(0_i64, |total, (index, value)| {
            let Some(next) = total.checked_add(value) else {
                return ControlFlow::Break(Err(MetricError::Overflow));
            };
            if next > limit {
                ControlFlow::Break(Ok((index, next)))
            } else {
                ControlFlow::Continue(next)
            }
        });

    match outcome {
        ControlFlow::Break(result) => result.map(Some),
        ControlFlow::Continue(_) => Ok(None),
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)]
pub struct SignChanges {
    pub seen: usize,
    pub changes: usize,
    last: Option<std::cmp::Ordering>,
}

pub fn sign_changes<I>(values: I) -> SignChanges
where
    I: IntoIterator<Item = i64>,
{
    values.into_iter().fold(SignChanges::default(), |mut state, value| {
        let sign = value.cmp(&0);
        if state.last.is_some_and(|previous| previous != sign) {
            state.changes += 1;
        }
        state.last = Some(sign);
        state.seen += 1;
        state
    })
}

#[cfg(test)]
mod tests {
    use super::{MetricError, Metrics, first_prefix_over, running_totals, sign_changes, summarize};

    #[test]
    fn empty_input_has_identity_summary() {
        assert_eq!(summarize([]).unwrap(), Metrics::default());
    }

    #[test]
    fn summary_preserves_prefix_invariant() {
        assert_eq!(
            summarize([3, -1, 5]).unwrap(),
            Metrics {
                count: 3,
                total: 7,
                minimum: Some(-1),
                maximum: Some(5),
            }
        );
    }

    #[test]
    fn running_totals_are_lazy_intermediate_states() {
        assert_eq!(
            running_totals([2, 3, -1]).collect::<Vec<_>>(),
            vec![Ok(2), Ok(5), Ok(4)]
        );
    }

    #[test]
    fn overflow_ends_the_running_stream_after_one_error() {
        let values = running_totals([i64::MAX, 1, 2]).collect::<Vec<_>>();
        assert_eq!(values, vec![Ok(i64::MAX), Err(MetricError::Overflow)]);
    }

    #[test]
    fn threshold_stops_at_first_crossing_prefix() {
        assert_eq!(first_prefix_over([2, 4, 8], 5), Ok(Some((1, 6))));
    }

    #[test]
    fn sign_change_accumulator_has_named_state() {
        assert_eq!(sign_changes([-1, -2, 3, 0, -1]).changes, 3);
    }
}
