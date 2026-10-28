#![forbid(unsafe_code)]

use std::sync::mpsc;
use std::thread;

pub const MAX_ITEMS: usize = 1024;
pub const MAX_WORKERS: usize = 64;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum MapOutcome {
    Squared(i64),
    Overflow,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum PipelineError {
    ZeroWorkers,
    TooManyWorkers { count: usize, limit: usize },
    TooManyItems { count: usize, limit: usize },
    WorkDisconnected { index: usize },
    ResultOutOfRange { index: usize, count: usize },
    DuplicateResult { index: usize },
    MissingResult { index: usize },
    WorkerPanicked { worker: usize },
}

#[must_use]
pub fn square(value: i64) -> MapOutcome {
    value
        .checked_mul(value)
        .map_or(MapOutcome::Overflow, MapOutcome::Squared)
}

pub fn map_bounded(
    values: Vec<i64>,
    workers: usize,
) -> Result<Vec<MapOutcome>, PipelineError> {
    if workers == 0 {
        return Err(PipelineError::ZeroWorkers);
    }
    if workers > MAX_WORKERS {
        return Err(PipelineError::TooManyWorkers {
            count: workers,
            limit: MAX_WORKERS,
        });
    }
    if values.len() > MAX_ITEMS {
        return Err(PipelineError::TooManyItems {
            count: values.len(),
            limit: MAX_ITEMS,
        });
    }

    let item_count = values.len();
    let (result_tx, result_rx) = mpsc::channel::<(usize, MapOutcome)>();
    let mut work_txs = Vec::with_capacity(workers);
    let mut handles = Vec::with_capacity(workers);

    for worker in 0..workers {
        let (work_tx, work_rx) = mpsc::sync_channel::<(usize, i64)>(1);
        let result_tx = result_tx.clone();
        work_txs.push(work_tx);
        handles.push((
            worker,
            thread::spawn(move || {
                while let Ok((index, value)) = work_rx.recv() {
                    if result_tx.send((index, square(value))).is_err() {
                        break;
                    }
                }
            }),
        ));
    }
    drop(result_tx);

    for (index, value) in values.into_iter().enumerate() {
        let worker = index % workers;
        if work_txs[worker].send((index, value)).is_err() {
            drop(work_txs);
            for (_, handle) in handles {
                let _ = handle.join();
            }
            return Err(PipelineError::WorkDisconnected { index });
        }
    }
    drop(work_txs);

    let mut slots: Vec<Option<MapOutcome>> = (0..item_count).map(|_| None).collect();
    let mut protocol_error = None;
    for (index, outcome) in result_rx {
        place_result(&mut slots, index, outcome, &mut protocol_error);
    }

    let mut first_panic = None;
    for (worker, handle) in handles {
        if handle.join().is_err() && first_panic.is_none() {
            first_panic = Some(PipelineError::WorkerPanicked { worker });
        }
    }

    if let Some(error) = protocol_error {
        return Err(error);
    }
    if let Some(error) = first_panic {
        return Err(error);
    }

    slots
        .into_iter()
        .enumerate()
        .map(|(index, value)| value.ok_or(PipelineError::MissingResult { index }))
        .collect()
}

fn place_result(
    slots: &mut [Option<MapOutcome>],
    index: usize,
    outcome: MapOutcome,
    first_error: &mut Option<PipelineError>,
) {
    let count = slots.len();
    let Some(slot) = slots.get_mut(index) else {
        first_error.get_or_insert(PipelineError::ResultOutOfRange { index, count });
        return;
    };
    if slot.is_some() {
        first_error.get_or_insert(PipelineError::DuplicateResult { index });
    } else {
        *slot = Some(outcome);
    }
}

#[cfg(test)]
mod tests {
    use super::{
        MAX_ITEMS, MAX_WORKERS, MapOutcome, PipelineError, map_bounded, place_result,
    };

    #[test]
    fn preserves_source_order_and_overflow() {
        assert_eq!(
            map_bounded(vec![3, i64::MAX, -4, 2], 3),
            Ok(vec![
                MapOutcome::Squared(9),
                MapOutcome::Overflow,
                MapOutcome::Squared(16),
                MapOutcome::Squared(4),
            ])
        );
    }

    #[test]
    fn handles_empty_input_and_capacity_one_work_channels() {
        assert_eq!(map_bounded(Vec::new(), 4), Ok(Vec::new()));
        assert_eq!(map_bounded((0..20).collect(), 1).expect("run").len(), 20);
    }

    #[test]
    fn validates_resource_bounds() {
        assert_eq!(map_bounded(vec![1], 0), Err(PipelineError::ZeroWorkers));
        assert!(matches!(
            map_bounded(vec![1], MAX_WORKERS + 1),
            Err(PipelineError::TooManyWorkers { .. })
        ));
        assert!(matches!(
            map_bounded(vec![0; MAX_ITEMS + 1], 2),
            Err(PipelineError::TooManyItems { .. })
        ));
    }

    #[test]
    fn result_assembly_rejects_duplicate_and_out_of_range_indices() {
        let mut slots = vec![None];
        let mut error = None;
        place_result(&mut slots, 0, MapOutcome::Squared(1), &mut error);
        place_result(&mut slots, 0, MapOutcome::Squared(2), &mut error);
        assert_eq!(error, Some(PipelineError::DuplicateResult { index: 0 }));
        assert_eq!(slots, vec![Some(MapOutcome::Squared(1))]);

        let mut error = None;
        place_result(&mut slots, 4, MapOutcome::Squared(4), &mut error);
        assert_eq!(
            error,
            Some(PipelineError::ResultOutOfRange { index: 4, count: 1 })
        );
    }
}
