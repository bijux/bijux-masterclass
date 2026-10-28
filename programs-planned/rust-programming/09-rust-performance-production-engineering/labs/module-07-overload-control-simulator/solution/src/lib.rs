use std::collections::{BTreeSet, VecDeque};

#[derive(Debug, Clone, Copy)]
pub struct Policy {
    pub queue_capacity: usize,
    pub service_per_tick: usize,
    pub retry_limit: u8,
    pub enter_recovery_at: usize,
    pub leave_recovery_below: usize,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Arrival {
    pub id: u64,
    pub attempt: u8,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Terminal {
    Completed(u64),
    Rejected(u64),
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum SimulationError {
    ZeroCapacity,
    InvertedRecoveryThresholds,
    RecoveryThresholdExceedsCapacity,
    DuplicateSourceId(u64),
    SourceAttemptMustBeZero(u64),
    CounterOverflow,
}

#[derive(Debug, Default, PartialEq, Eq)]
pub struct Report {
    pub source_offered: usize,
    pub attempts: usize,
    pub admitted_attempts: usize,
    pub completed: usize,
    pub rejected: usize,
    pub retries_scheduled: usize,
    pub max_queue: usize,
    pub recovery_ticks: usize,
    pub terminal: Vec<Terminal>,
}

pub fn simulate(
    arrivals_by_tick: &[Vec<Arrival>],
    policy: Policy,
) -> Result<Report, SimulationError> {
    if policy.queue_capacity == 0 || policy.service_per_tick == 0 {
        return Err(SimulationError::ZeroCapacity);
    }
    if policy.leave_recovery_below > policy.enter_recovery_at {
        return Err(SimulationError::InvertedRecoveryThresholds);
    }
    if policy.enter_recovery_at > policy.queue_capacity {
        return Err(SimulationError::RecoveryThresholdExceedsCapacity);
    }

    let mut source_ids = BTreeSet::new();
    for arrival in arrivals_by_tick.iter().flatten() {
        if arrival.attempt != 0 {
            return Err(SimulationError::SourceAttemptMustBeZero(arrival.id));
        }
        if !source_ids.insert(arrival.id) {
            return Err(SimulationError::DuplicateSourceId(arrival.id));
        }
    }

    let mut report = Report {
        source_offered: source_ids.len(),
        ..Report::default()
    };
    let mut queue = VecDeque::new();
    let mut retry_next = Vec::<Arrival>::new();
    let mut recovering = false;
    let mut tick = 0_usize;

    while tick < arrivals_by_tick.len() || !queue.is_empty() || !retry_next.is_empty() {
        let mut offered = std::mem::take(&mut retry_next);
        if let Some(source) = arrivals_by_tick.get(tick) {
            offered.extend_from_slice(source);
        }
        report.attempts = report
            .attempts
            .checked_add(offered.len())
            .ok_or(SimulationError::CounterOverflow)?;

        if queue.len() >= policy.enter_recovery_at {
            recovering = true;
        } else if queue.len() <= policy.leave_recovery_below {
            recovering = false;
        }
        if recovering {
            report.recovery_ticks = report
                .recovery_ticks
                .checked_add(1)
                .ok_or(SimulationError::CounterOverflow)?;
        }

        let effective_capacity = if recovering {
            (policy.queue_capacity / 2).max(1)
        } else {
            policy.queue_capacity
        };

        for arrival in offered {
            if queue.len() < effective_capacity {
                queue.push_back(arrival);
                report.admitted_attempts = report
                    .admitted_attempts
                    .checked_add(1)
                    .ok_or(SimulationError::CounterOverflow)?;
            } else if arrival.attempt < policy.retry_limit {
                retry_next.push(Arrival {
                    id: arrival.id,
                    attempt: arrival
                        .attempt
                        .checked_add(1)
                        .ok_or(SimulationError::CounterOverflow)?,
                });
                report.retries_scheduled = report
                    .retries_scheduled
                    .checked_add(1)
                    .ok_or(SimulationError::CounterOverflow)?;
            } else {
                report.rejected = report
                    .rejected
                    .checked_add(1)
                    .ok_or(SimulationError::CounterOverflow)?;
                report.terminal.push(Terminal::Rejected(arrival.id));
            }
        }

        report.max_queue = report.max_queue.max(queue.len());
        for _ in 0..policy.service_per_tick {
            let Some(arrival) = queue.pop_front() else {
                break;
            };
            report.completed = report
                .completed
                .checked_add(1)
                .ok_or(SimulationError::CounterOverflow)?;
            report.terminal.push(Terminal::Completed(arrival.id));
        }
        tick = tick
            .checked_add(1)
            .ok_or(SimulationError::CounterOverflow)?;
    }

    report.terminal.sort_by_key(|terminal| match terminal {
        Terminal::Completed(id) | Terminal::Rejected(id) => *id,
    });
    debug_assert_eq!(
        report.completed + report.rejected,
        report.source_offered
    );
    Ok(report)
}

#[cfg(test)]
mod tests {
    use super::*;

    fn policy() -> Policy {
        Policy {
            queue_capacity: 4,
            service_per_tick: 1,
            retry_limit: 1,
            enter_recovery_at: 3,
            leave_recovery_below: 1,
        }
    }

    #[test]
    fn every_source_request_reaches_one_terminal_outcome() {
        let arrivals = vec![
            vec![
                Arrival { id: 1, attempt: 0 },
                Arrival { id: 2, attempt: 0 },
                Arrival { id: 3, attempt: 0 },
                Arrival { id: 4, attempt: 0 },
                Arrival { id: 5, attempt: 0 },
            ],
            Vec::new(),
            Vec::new(),
        ];
        let report = simulate(&arrivals, policy()).expect("valid simulation");
        assert_eq!(report.source_offered, 5);
        assert_eq!(report.terminal.len(), 5);
        assert_eq!(report.completed + report.rejected, 5);
        assert_eq!(report.attempts, 5 + report.retries_scheduled);
        assert!(report.max_queue <= 4);
    }

    #[test]
    fn duplicate_source_identity_is_rejected() {
        let arrivals = vec![vec![
            Arrival { id: 1, attempt: 0 },
            Arrival { id: 1, attempt: 0 },
        ]];
        assert_eq!(
            simulate(&arrivals, policy()),
            Err(SimulationError::DuplicateSourceId(1))
        );
    }

    #[test]
    fn invalid_thresholds_are_rejected() {
        let mut invalid = policy();
        invalid.leave_recovery_below = 4;
        invalid.enter_recovery_at = 2;
        assert_eq!(
            simulate(&[], invalid),
            Err(SimulationError::InvertedRecoveryThresholds)
        );
    }
}
