#![forbid(unsafe_code)]

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

#[cfg(test)]
mod tests {
    use super::chunk_len;

    #[test]
    fn baseline_chunking_handles_more_workers_than_items() {
        assert_eq!(chunk_len(3, 8), Some(1));
        assert_eq!(chunk_len(0, 8), None);
        assert_eq!(chunk_len(3, 0), None);
    }
}
