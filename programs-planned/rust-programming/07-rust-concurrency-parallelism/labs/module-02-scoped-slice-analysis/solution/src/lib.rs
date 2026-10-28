#![forbid(unsafe_code)]

use std::thread;

pub const MAX_WORKERS: usize = 64;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Summary {
    pub count: usize,
    pub sum: i64,
    pub min: i32,
    pub max: i32,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum AnalysisError {
    ZeroWorkers,
    TooManyWorkers { count: usize, limit: usize },
    EmptyChunk,
    SumOverflow,
    WorkerPanicked,
}

#[must_use]
pub fn chunk_len(item_count: usize, workers: usize) -> Option<usize> {
    if item_count == 0 || workers == 0 {
        None
    } else {
        Some(item_count.div_ceil(workers))
    }
}

fn summarize_chunk(chunk: &[i32]) -> Result<Summary, AnalysisError> {
    let mut iter = chunk.iter().copied();
    let first = iter.next().ok_or(AnalysisError::EmptyChunk)?;
    let mut summary = Summary {
        count: 1,
        sum: i64::from(first),
        min: first,
        max: first,
    };
    for value in iter {
        summary.count += 1;
        summary.sum = summary
            .sum
            .checked_add(i64::from(value))
            .ok_or(AnalysisError::SumOverflow)?;
        summary.min = summary.min.min(value);
        summary.max = summary.max.max(value);
    }
    Ok(summary)
}

fn combine(left: Summary, right: Summary) -> Result<Summary, AnalysisError> {
    Ok(Summary {
        count: left.count + right.count,
        sum: left
            .sum
            .checked_add(right.sum)
            .ok_or(AnalysisError::SumOverflow)?,
        min: left.min.min(right.min),
        max: left.max.max(right.max),
    })
}

pub fn summarize(values: &[i32], workers: usize) -> Result<Option<Summary>, AnalysisError> {
    validate_workers(workers)?;
    if values.is_empty() {
        return Ok(None);
    }

    let size = values.len().div_ceil(workers);
    thread::scope(|scope| {
        let handles: Vec<_> = values
            .chunks(size)
            .map(|chunk| scope.spawn(move || summarize_chunk(chunk)))
            .collect();

        let mut combined: Option<Summary> = None;
        let mut panicked = false;
        let mut domain_error = None;
        for handle in handles {
            match handle.join() {
                Ok(Ok(part)) if domain_error.is_none() => {
                    combined = match combined {
                        None => Some(part),
                        Some(current) => match combine(current, part) {
                            Ok(value) => Some(value),
                            Err(error) => {
                                domain_error = Some(error);
                                Some(current)
                            }
                        },
                    };
                }
                Ok(Ok(_)) => {}
                Ok(Err(error)) => {
                    domain_error.get_or_insert(error);
                }
                Err(_) => panicked = true,
            }
        }

        if panicked {
            Err(AnalysisError::WorkerPanicked)
        } else if let Some(error) = domain_error {
            Err(error)
        } else {
            Ok(combined)
        }
    })
}

pub fn normalize(values: &mut [i64], workers: usize) -> Result<(), AnalysisError> {
    validate_workers(workers)?;
    if values.is_empty() {
        return Ok(());
    }

    let size = values.len().div_ceil(workers);
    thread::scope(|scope| {
        for chunk in values.chunks_mut(size) {
            scope.spawn(move || {
                for value in chunk {
                    *value = value.saturating_abs();
                }
            });
        }
    });
    Ok(())
}

fn validate_workers(workers: usize) -> Result<(), AnalysisError> {
    if workers == 0 {
        Err(AnalysisError::ZeroWorkers)
    } else if workers > MAX_WORKERS {
        Err(AnalysisError::TooManyWorkers {
            count: workers,
            limit: MAX_WORKERS,
        })
    } else {
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::{AnalysisError, MAX_WORKERS, Summary, normalize, summarize};

    #[test]
    fn summarize_matches_across_worker_counts() {
        let values = [5, -2, 9, 1, -7, 4, 8];
        let expected = Some(Summary {
            count: 7,
            sum: 18,
            min: -7,
            max: 9,
        });
        for workers in [1, 2, 3, 20] {
            assert_eq!(summarize(&values, workers), Ok(expected));
        }
        assert_eq!(values[0], 5, "parent can reuse source after scope");
    }

    #[test]
    fn normalize_uses_disjoint_mutable_regions() {
        let mut values = [i64::MIN, -4, 0, 9, -12];
        normalize(&mut values, 8).expect("valid worker count");
        assert_eq!(values, [i64::MAX, 4, 0, 9, 12]);
    }

    #[test]
    fn handles_empty_and_invalid_worker_counts() {
        assert_eq!(summarize(&[], 3), Ok(None));
        assert_eq!(summarize(&[1], 0), Err(AnalysisError::ZeroWorkers));
        assert!(matches!(
            summarize(&[1], MAX_WORKERS + 1),
            Err(AnalysisError::TooManyWorkers { .. })
        ));
    }
}
