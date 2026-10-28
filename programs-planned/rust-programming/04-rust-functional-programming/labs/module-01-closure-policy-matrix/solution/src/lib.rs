#![forbid(unsafe_code)]

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Job {
    pub label: String,
    pub urgency: u8,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Decision {
    pub normalized_label: String,
    pub score: i64,
}

pub fn resolve_or_else<T, F>(value: Option<T>, fallback: F) -> T
where
    F: FnOnce() -> T,
{
    value.unwrap_or_else(fallback)
}

pub fn classify_all<T, R, F>(items: &[T], classifier: F) -> Vec<R>
where
    F: FnMut(&T) -> R,
{
    items.iter().map(classifier).collect()
}

pub struct Policy<N, S> {
    normalizer: N,
    scorer: S,
}

impl<N, S> Policy<N, S> {
    pub fn new(normalizer: N, scorer: S) -> Self {
        Self { normalizer, scorer }
    }
}

impl<N, S> Policy<N, S>
where
    N: FnMut(String) -> String,
    S: FnMut(&Job) -> i64,
{
    pub fn evaluate<I>(&mut self, jobs: I) -> Vec<Decision>
    where
        I: IntoIterator<Item = Job>,
    {
        let normalizer = &mut self.normalizer;
        let scorer = &mut self.scorer;
        jobs.into_iter()
            .map(|mut job| {
                job.label = normalizer(job.label);
                let score = scorer(&job);
                Decision {
                    normalized_label: job.label,
                    score,
                }
            })
            .collect()
    }
}

pub fn finalize_once<F>(report: String, finalizer: F) -> usize
where
    F: FnOnce(String) -> usize,
{
    finalizer(report)
}

#[cfg(test)]
mod tests {
    use super::{Decision, Job, Policy, classify_all, finalize_once, resolve_or_else};
    use std::cell::Cell;

    #[test]
    fn fallback_is_lazy_and_called_at_most_once() {
        let calls = Cell::new(0);
        let present = resolve_or_else(Some(7), || {
            calls.set(calls.get() + 1);
            9
        });
        assert_eq!(present, 7);
        assert_eq!(calls.get(), 0);

        let missing = resolve_or_else(None, || {
            calls.set(calls.get() + 1);
            9
        });
        assert_eq!(missing, 9);
        assert_eq!(calls.get(), 1);
    }

    #[test]
    fn stateful_classifier_preserves_source_order() {
        let mut calls = 0;
        let output = classify_all(&[2, 4, 6], |value| {
            calls += 1;
            *value + calls
        });
        assert_eq!(output, vec![3, 6, 9]);
        assert_eq!(calls, 3);
    }

    #[test]
    fn policy_normalizes_before_scoring() {
        let mut policy = Policy::new(
            |value: String| value.trim().to_ascii_lowercase(),
            |job: &Job| i64::from(job.urgency) * 10 + job.label.len() as i64,
        );
        let output = policy.evaluate([
            Job {
                label: " A ".to_owned(),
                urgency: 2,
            },
            Job {
                label: "Blue".to_owned(),
                urgency: 1,
            },
        ]);
        assert_eq!(
            output,
            vec![
                Decision {
                    normalized_label: "a".to_owned(),
                    score: 21,
                },
                Decision {
                    normalized_label: "blue".to_owned(),
                    score: 14,
                },
            ]
        );
    }

    #[test]
    fn finalizer_may_consume_owned_capture() {
        let suffix = String::from("!");
        let length = finalize_once(String::from("done"), move |mut report| {
            report.push_str(&suffix);
            report.len()
        });
        assert_eq!(length, 5);
    }
}
