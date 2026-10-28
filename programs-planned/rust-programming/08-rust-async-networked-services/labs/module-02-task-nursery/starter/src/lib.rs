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

pub fn validate_job_count(count: usize) -> Result<(), &'static str> {
    if count <= 32 {
        Ok(())
    } else {
        Err("at most 32 jobs are accepted")
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn job_bound_is_explicit() {
        assert!(validate_job_count(32).is_ok());
        assert!(validate_job_count(33).is_err());
    }
}
