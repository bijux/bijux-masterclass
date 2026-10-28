use std::{collections::{HashMap, HashSet}, future::Future};
use tokio::task::JoinSet;
use tokio_util::sync::CancellationToken;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Policy {
    CompleteAll,
    FailFast,
}

#[derive(Debug, PartialEq, Eq)]
pub enum Outcome<T, E> {
    Completed(T),
    Failed(E),
    Panicked,
    Cancelled,
}

#[derive(Debug, PartialEq, Eq)]
pub struct IndexedOutcome<T, E> {
    pub index: usize,
    pub outcome: Outcome<T, E>,
}

pub async fn run<I, F, T, E>(jobs: I, policy: Policy) -> Result<Vec<IndexedOutcome<T, E>>, &'static str>
where
    I: IntoIterator<Item = (usize, F)>,
    F: Future<Output = Result<T, E>> + Send + 'static,
    T: Send + 'static,
    E: Send + 'static,
{
    let jobs: Vec<_> = jobs.into_iter().collect();
    if jobs.len() > 32 {
        return Err("at most 32 jobs are accepted");
    }
    let mut indices = HashSet::with_capacity(jobs.len());
    if jobs.iter().any(|(index, _)| !indices.insert(*index)) {
        return Err("source indices must be unique");
    }

    let cancel = CancellationToken::new();
    let mut set = JoinSet::new();
    let mut task_indices = HashMap::new();
    for (index, future) in jobs {
        let child = cancel.child_token();
        let abort_handle = set.spawn(async move {
            let outcome = tokio::select! {
                result = future => Some(result),
                () = child.cancelled() => None,
            };
            (index, outcome)
        });
        debug_assert!(task_indices.insert(abort_handle.id(), index).is_none());
    }
    let mut results = Vec::new();
    while let Some(joined) = set.join_next_with_id().await {
        match joined {
            Ok((id, (index, Some(Ok(value))))) => {
                debug_assert!(task_indices.remove(&id).is_some());
                results.push(IndexedOutcome { index, outcome: Outcome::Completed(value) });
            }
            Ok((id, (index, Some(Err(error))))) => {
                debug_assert!(task_indices.remove(&id).is_some());
                if policy == Policy::FailFast {
                    cancel.cancel();
                }
                results.push(IndexedOutcome { index, outcome: Outcome::Failed(error) });
            }
            Ok((id, (index, None))) => {
                debug_assert!(task_indices.remove(&id).is_some());
                results.push(IndexedOutcome { index, outcome: Outcome::Cancelled });
            }
            Err(error) => {
                if policy == Policy::FailFast {
                    cancel.cancel();
                }
                let index = task_indices
                    .remove(&error.id())
                    .ok_or("task identity missing from nursery")?;
                results.push(IndexedOutcome {
                    index,
                    outcome: if error.is_cancelled() { Outcome::Cancelled } else { Outcome::Panicked },
                });
            }
        }
    }
    results.sort_by_key(|result| result.index);
    Ok(results)
}

#[cfg(test)]
mod tests {
    use super::*;
    use tokio::sync::Notify;
    use std::sync::Arc;

    #[tokio::test]
    async fn completion_order_does_not_change_result_order() {
        let gates: Vec<_> = (0..3).map(|_| Arc::new(Notify::new())).collect();
        let jobs: Vec<_> = gates.iter().enumerate().map(|(index, gate)| {
            let gate = Arc::clone(gate);
            (index, async move { gate.notified().await; Ok::<_, ()>(index) })
        }).collect();
        let task = tokio::spawn(run(jobs, Policy::CompleteAll));
        gates[2].notify_one(); gates[1].notify_one(); gates[0].notify_one();
        let output = task.await.unwrap().unwrap();
        assert_eq!(output.iter().map(|item| item.index).collect::<Vec<_>>(), vec![0,1,2]);
    }

    #[tokio::test]
    async fn fail_fast_still_returns_one_outcome_per_job() {
        use std::pin::Pin;

        type Job = Pin<Box<dyn Future<Output = Result<u64, &'static str>> + Send>>;
        let jobs: Vec<(usize, Job)> = vec![
            (0, Box::pin(async { Err("failed") })),
            (
                1,
                Box::pin(async {
                    tokio::task::yield_now().await;
                    Ok(1)
                }),
            ),
        ];
        let output = run(jobs, Policy::FailFast).await.unwrap();
        assert_eq!(output.len(), 2);
    }

    #[tokio::test]
    async fn duplicate_source_indices_are_rejected_before_spawn() {
        let jobs = vec![
            (0, std::future::ready(Ok::<u64, ()>(1))),
            (0, std::future::ready(Ok::<u64, ()>(2))),
        ];
        assert_eq!(
            run(jobs, Policy::CompleteAll).await,
            Err("source indices must be unique")
        );
    }

}
