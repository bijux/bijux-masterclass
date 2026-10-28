#![forbid(unsafe_code)]

use rayon::prelude::*;
use rayon::{ThreadPool, ThreadPoolBuilder};
use std::collections::BTreeMap;

pub const MAX_LABELS: usize = 1_000_000;
pub const MAX_THREADS: usize = 64;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum HistogramError {
    ZeroThreads,
    TooManyThreads { count: usize, limit: usize },
    TooManyLabels { count: usize, limit: usize },
    PoolBuild(String),
}

#[must_use]
pub fn sequential(labels: &[String]) -> BTreeMap<String, usize> {
    labels.iter().fold(BTreeMap::new(), |mut map, label| {
        *map.entry(label.clone()).or_default() += 1;
        map
    })
}

pub fn build_pool(threads: usize) -> Result<ThreadPool, HistogramError> {
    if threads == 0 {
        return Err(HistogramError::ZeroThreads);
    }
    if threads > MAX_THREADS {
        return Err(HistogramError::TooManyThreads {
            count: threads,
            limit: MAX_THREADS,
        });
    }
    ThreadPoolBuilder::new()
        .num_threads(threads)
        .build()
        .map_err(|error| HistogramError::PoolBuild(error.to_string()))
}

fn merge(mut left: BTreeMap<String, usize>, right: BTreeMap<String, usize>) -> BTreeMap<String, usize> {
    for (key, count) in right { *left.entry(key).or_default() += count; }
    left
}

pub fn parallel(pool: &ThreadPool, labels: &[String], cutoff: usize) -> Result<BTreeMap<String, usize>, HistogramError> {
    if labels.len() > MAX_LABELS {
        return Err(HistogramError::TooManyLabels { count: labels.len(), limit: MAX_LABELS });
    }
    if labels.len() < cutoff { return Ok(sequential(labels)); }
    Ok(pool.install(|| {
        labels.par_iter()
            .fold(BTreeMap::new, |mut local, label| {
                *local.entry(label.clone()).or_default() += 1;
                local
            })
            .reduce(BTreeMap::new, merge)
    }))
}

#[cfg(test)]
mod tests {
    use super::{HistogramError, MAX_THREADS, build_pool, parallel, sequential};

    fn fixture(size: usize) -> Vec<String> {
        (0..size).map(|index| format!("label-{}", index % 17)).collect()
    }

    #[test]
    fn parallel_matches_oracle_across_pool_widths() {
        for size in [0, 1, 17, 255, 256, 10_000] {
            let labels = fixture(size);
            let expected = sequential(&labels);
            for threads in [1, 2, 4] {
                let pool = build_pool(threads).expect("pool builds");
                assert_eq!(parallel(&pool, &labels, 256).expect("bounded"), expected);
            }
        }
    }

    #[test]
    fn cutoff_paths_are_identical() {
        let labels = fixture(300);
        let pool = build_pool(3).expect("pool builds");
        assert_eq!(parallel(&pool, &labels, 1000), parallel(&pool, &labels, 0));
    }

    #[test]
    fn pool_width_is_a_product_bound() {
        assert!(matches!(build_pool(0), Err(HistogramError::ZeroThreads)));
        assert!(matches!(
            build_pool(MAX_THREADS + 1),
            Err(HistogramError::TooManyThreads { .. })
        ));
    }
}
