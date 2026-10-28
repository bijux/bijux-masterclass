#![forbid(unsafe_code)]
//! Starter domain for the closure-policy laboratory.

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

pub struct Policy<N, S> {
    normalizer: N,
    scorer: S,
}

impl<N, S> Policy<N, S> {
    pub fn new(normalizer: N, scorer: S) -> Self {
        Self { normalizer, scorer }
    }

    pub fn into_parts(self) -> (N, S) {
        (self.normalizer, self.scorer)
    }
}

#[cfg(test)]
mod tests {
    use super::{Job, Policy};

    #[test]
    fn starter_exposes_concrete_callable_storage() {
        let policy = Policy::new(|value: String| value, |job: &Job| i64::from(job.urgency));
        let (_normalizer, _scorer) = policy.into_parts();
    }
}
