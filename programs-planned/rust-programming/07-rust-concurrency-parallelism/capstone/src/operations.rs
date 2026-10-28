use crate::domain::{Job, Operation};
use crate::error::DomainError;

pub const MAX_SORT_ITEMS: usize = 4096;
pub const MAX_PRIME_LIMIT: u64 = 250_000;

pub fn execute(job: &Job) -> Result<String, DomainError> {
    match job.operation {
        Operation::Checksum => Ok(format!("{:016x}", fnv1a(job.payload.as_bytes()))),
        Operation::WordCount => Ok(job.payload.split_whitespace().count().to_string()),
        Operation::SortIntegers => sort_integers(&job.payload),
        Operation::PrimeCount => prime_count(&job.payload),
        Operation::Panic => panic!("BatchWeave injected panic for job {}", job.id),
    }
}

#[must_use]
pub fn fnv1a(bytes: &[u8]) -> u64 {
    bytes.iter().fold(0xcbf_29ce_4842_2325, |hash, byte| {
        (hash ^ u64::from(*byte)).wrapping_mul(0x100_0000_01b3)
    })
}

fn sort_integers(payload: &str) -> Result<String, DomainError> {
    if payload.trim().is_empty() {
        return Ok(String::new());
    }
    let tokens: Vec<_> = payload.split(',').collect();
    if tokens.len() > MAX_SORT_ITEMS {
        return Err(DomainError::TooManyIntegers {
            count: tokens.len(),
            limit: MAX_SORT_ITEMS,
        });
    }
    let mut values = Vec::with_capacity(tokens.len());
    for token in tokens {
        let trimmed = token.trim();
        let value = trimmed.parse::<i64>().map_err(|_| DomainError::InvalidInteger {
            token: trimmed.to_owned(),
        })?;
        values.push(value);
    }
    values.sort_unstable();
    Ok(values
        .into_iter()
        .map(|value| value.to_string())
        .collect::<Vec<_>>()
        .join(","))
}

fn prime_count(payload: &str) -> Result<String, DomainError> {
    let trimmed = payload.trim();
    let limit = trimmed.parse::<u64>().map_err(|_| DomainError::PrimeLimitInvalid {
        value: trimmed.to_owned(),
    })?;
    if limit > MAX_PRIME_LIMIT {
        return Err(DomainError::PrimeLimitTooLarge {
            value: limit,
            limit: MAX_PRIME_LIMIT,
        });
    }
    Ok((2..=limit).filter(|value| is_prime(*value)).count().to_string())
}

fn is_prime(value: u64) -> bool {
    if value < 2 {
        return false;
    }
    if value == 2 {
        return true;
    }
    if value % 2 == 0 {
        return false;
    }
    let mut divisor = 3u64;
    while divisor <= value / divisor {
        if value % divisor == 0 {
            return false;
        }
        divisor += 2;
    }
    true
}

#[cfg(test)]
mod tests {
    use super::{execute, fnv1a};
    use crate::domain::{Job, JobId, Operation};
    use crate::error::DomainError;

    fn job(operation: Operation, payload: &str) -> Job {
        Job {
            index: 0,
            id: JobId::new("job").expect("valid id"),
            operation,
            payload: payload.to_owned(),
        }
    }

    #[test]
    fn operations_are_deterministic_and_bounded() {
        assert_eq!(execute(&job(Operation::Checksum, "abc")), Ok(format!("{:016x}", fnv1a(b"abc"))));
        assert_eq!(execute(&job(Operation::WordCount, "one  two\nthree")), Ok("3".to_owned()));
        assert_eq!(execute(&job(Operation::SortIntegers, "3,-1,2")), Ok("-1,2,3".to_owned()));
        assert_eq!(execute(&job(Operation::PrimeCount, "10")), Ok("4".to_owned()));
    }

    #[test]
    fn malformed_integer_is_a_domain_error() {
        assert_eq!(execute(&job(Operation::SortIntegers, "1,nope")), Err(DomainError::InvalidInteger { token: "nope".to_owned() }));
    }
}
