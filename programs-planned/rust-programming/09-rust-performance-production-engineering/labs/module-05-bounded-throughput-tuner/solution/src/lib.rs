use std::sync::Arc;
use std::time::{Duration, Instant};
use tokio::sync::{Semaphore, mpsc};

#[derive(Debug, Clone, Copy)]
pub struct Tuning {
    pub queue_capacity: usize,
    pub max_active: usize,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Outcome {
    Completed { index: usize, value: u64 },
    Failed { index: usize, message: &'static str },
    Rejected { index: usize },
}

impl Outcome {
    fn index(&self) -> usize {
        match self {
            Self::Completed { index, .. }
            | Self::Failed { index, .. }
            | Self::Rejected { index } => *index,
        }
    }
}

#[derive(Debug, Clone, Copy)]
pub struct PhaseSample {
    pub index: usize,
    pub queue_wait: Duration,
    pub service: Duration,
}

#[derive(Debug)]
pub struct Report {
    pub offered: usize,
    pub accepted: usize,
    pub completed: usize,
    pub failed: usize,
    pub rejected: usize,
    pub outcomes: Vec<Outcome>,
    pub samples: Vec<PhaseSample>,
}

pub async fn run(values: Vec<u64>, tuning: Tuning) -> Result<Report, &'static str> {
    if tuning.queue_capacity == 0 || tuning.max_active == 0 {
        return Err("capacities must be nonzero");
    }

    let offered = values.len();
    let (sender, mut receiver) =
        mpsc::channel::<(usize, u64, Instant)>(tuning.queue_capacity);
    let permits = Arc::new(Semaphore::new(tuning.max_active));
    let mut outcomes = vec![None; offered];
    let mut rejected = 0_usize;

    // The submission phase models one instantaneous burst. No receiver runs until
    // the burst has been offered, so admission is deterministic for a fixed queue.
    for (index, value) in values.into_iter().enumerate() {
        match sender.try_send((index, value, Instant::now())) {
            Ok(()) => {}
            Err(_) => {
                outcomes[index] = Some(Outcome::Rejected { index });
                rejected += 1;
            }
        }
    }
    drop(sender);

    let mut tasks = Vec::with_capacity(offered.saturating_sub(rejected));
    while let Some((index, value, queued_at)) = receiver.recv().await {
        let permit = Arc::clone(&permits)
            .acquire_owned()
            .await
            .map_err(|_| "semaphore closed")?;
        tasks.push(tokio::spawn(async move {
            let queue_wait = queued_at.elapsed();
            let started = Instant::now();
            tokio::time::sleep(Duration::from_millis(1)).await;
            let result = value.checked_mul(2);
            let service = started.elapsed();
            drop(permit);
            (
                index,
                result,
                PhaseSample {
                    index,
                    queue_wait,
                    service,
                },
            )
        }));
    }

    let mut samples = Vec::with_capacity(tasks.len());
    for task in tasks {
        let (index, value, sample) = task.await.map_err(|_| "worker panicked")?;
        outcomes[index] = Some(match value {
            Some(value) => Outcome::Completed { index, value },
            None => Outcome::Failed {
                index,
                message: "value overflow",
            },
        });
        samples.push(sample);
    }

    let outcomes: Vec<_> = outcomes
        .into_iter()
        .map(|outcome| outcome.ok_or("missing terminal outcome"))
        .collect::<Result<_, _>>()?;
    debug_assert!(outcomes
        .iter()
        .enumerate()
        .all(|(index, outcome)| outcome.index() == index));

    let completed = outcomes
        .iter()
        .filter(|outcome| matches!(outcome, Outcome::Completed { .. }))
        .count();
    let failed = outcomes
        .iter()
        .filter(|outcome| matches!(outcome, Outcome::Failed { .. }))
        .count();
    let accepted = completed
        .checked_add(failed)
        .ok_or("accepted count overflow")?;

    Ok(Report {
        offered,
        accepted,
        completed,
        failed,
        rejected,
        outcomes,
        samples,
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn accounting_is_complete_and_source_ordered() {
        let report = run(
            vec![5, 4, 3, 2, 1],
            Tuning {
                queue_capacity: 3,
                max_active: 2,
            },
        )
        .await
        .expect("valid run");
        assert_eq!(report.outcomes.len(), report.offered);
        assert_eq!(
            report.completed + report.failed + report.rejected,
            report.offered
        );
        assert_eq!(report.accepted, report.completed + report.failed);
        for (index, outcome) in report.outcomes.iter().enumerate() {
            assert_eq!(outcome.index(), index);
        }
    }

    #[tokio::test]
    async fn arithmetic_failure_is_terminal_not_lost() {
        let report = run(
            vec![u64::MAX],
            Tuning {
                queue_capacity: 1,
                max_active: 1,
            },
        )
        .await
        .expect("valid run");
        assert_eq!(report.failed, 1);
        assert!(matches!(report.outcomes[0], Outcome::Failed { .. }));
    }

    #[tokio::test]
    async fn zero_capacity_is_rejected() {
        assert!(
            run(
                vec![1],
                Tuning {
                    queue_capacity: 0,
                    max_active: 1,
                },
            )
            .await
            .is_err()
        );
    }
}
