use crate::domain::{Job, JobOutcome, OutcomeKind, RunReport, Summary};
use crate::error::RunError;
use rayon::prelude::*;
use rayon::ThreadPoolBuilder;
use std::collections::BTreeMap;
use std::num::NonZeroUsize;

#[derive(Default)]
struct PartialSummary {
    by_status: BTreeMap<String, usize>,
    by_operation: BTreeMap<String, usize>,
    total: usize,
}

impl PartialSummary {
    fn add(mut self, outcome: &JobOutcome) -> Self {
        self.total += 1;
        *self
            .by_status
            .entry(outcome.kind.status().to_owned())
            .or_default() += 1;
        *self
            .by_operation
            .entry(outcome.operation.as_str().to_owned())
            .or_default() += 1;
        self
    }

    fn merge(mut self, other: Self) -> Self {
        self.total += other.total;
        for (key, value) in other.by_status {
            *self.by_status.entry(key).or_default() += value;
        }
        for (key, value) in other.by_operation {
            *self.by_operation.entry(key).or_default() += value;
        }
        self
    }
}

pub(crate) fn summarize_parallel(
    outcomes: &[JobOutcome],
    threads: NonZeroUsize,
) -> Result<Summary, RunError> {
    if outcomes.len() < 128 {
        return Ok(summarize_sequential(outcomes));
    }

    let pool = ThreadPoolBuilder::new()
        .num_threads(threads.get())
        .build()
        .map_err(|error| RunError::ReportPool(error.to_string()))?;

    let partial = pool.install(|| {
        outcomes
            .par_iter()
            .fold(PartialSummary::default, PartialSummary::add)
            .reduce(PartialSummary::default, PartialSummary::merge)
    });
    Ok(Summary {
        total: partial.total,
        by_status: partial.by_status,
        by_operation: partial.by_operation,
    })
}

#[must_use]
pub fn summarize_sequential(outcomes: &[JobOutcome]) -> Summary {
    let partial = outcomes.iter().fold(PartialSummary::default(), PartialSummary::add);
    Summary {
        total: partial.total,
        by_status: partial.by_status,
        by_operation: partial.by_operation,
    }
}

#[must_use]
pub fn render_inspection(jobs: &[Job]) -> String {
    let mut by_operation: BTreeMap<&str, usize> = BTreeMap::new();
    let total_payload: usize = jobs.iter().map(|job| job.payload.len()).sum();
    for job in jobs {
        *by_operation.entry(job.operation.as_str()).or_default() += 1;
    }
    let mut output = format!(
        "manifest\tjobs={}\tpayload_bytes={}\n",
        jobs.len(), total_payload
    );
    for (operation, count) in by_operation {
        output.push_str(&format!("operation\t{operation}\t{count}\n"));
    }
    output
}

#[must_use]
pub fn render_report(report: &RunReport) -> String {
    let mut output = String::from("index\tid\toperation\tstatus\tdetail\n");
    for outcome in &report.outcomes {
        output.push_str(&format!(
            "{}\t{}\t{}\t{}\t{}\n",
            outcome.index,
            outcome.id,
            outcome.operation,
            outcome.kind.status(),
            sanitize(outcome.kind.detail())
        ));
    }
    output.push_str(&format!("summary\ttotal\t{}\n", report.summary.total));
    for (status, count) in &report.summary.by_status {
        output.push_str(&format!("summary-status\t{status}\t{count}\n"));
    }
    for (operation, count) in &report.summary.by_operation {
        output.push_str(&format!("summary-operation\t{operation}\t{count}\n"));
    }
    let metrics = report.live_metrics_at_end;
    output.push_str(&format!(
        "live-metrics\tsubmitted={}\tstarted={}\tcompleted={}\tfailed={}\tpanicked={}\tcancelled={}\n",
        metrics.submitted,
        metrics.started,
        metrics.completed,
        metrics.failed,
        metrics.panicked,
        metrics.cancelled
    ));
    output
}

fn sanitize(value: &str) -> String {
    value
        .chars()
        .map(|character| match character {
            '\t' | '\n' | '\r' => ' ',
            other => other,
        })
        .collect()
}

#[must_use]
pub fn report_is_accepted(report: &RunReport) -> bool {
    report
        .outcomes
        .iter()
        .all(|outcome| matches!(&outcome.kind, OutcomeKind::Completed(_)))
}

#[cfg(test)]
mod tests {
    use super::{summarize_parallel, summarize_sequential};
    use crate::domain::{JobId, JobOutcome, Operation, OutcomeKind};
    use std::num::NonZeroUsize;

    #[test]
    fn parallel_summary_matches_sequential_oracle() {
        let outcomes: Vec<_> = (0..1000)
            .map(|index| JobOutcome {
                index,
                id: JobId::new(format!("job-{index}")).expect("valid id"),
                operation: if index % 2 == 0 { Operation::Checksum } else { Operation::WordCount },
                kind: if index % 7 == 0 {
                    OutcomeKind::DomainFailed("failure".to_owned())
                } else {
                    OutcomeKind::Completed(index.to_string())
                },
            })
            .collect();
        let expected = summarize_sequential(&outcomes);
        for threads in [1, 2, 4] {
            let observed = summarize_parallel(
                &outcomes,
                NonZeroUsize::new(threads).expect("nonzero"),
            )
            .expect("pool builds");
            assert_eq!(observed, expected);
        }
    }
}
