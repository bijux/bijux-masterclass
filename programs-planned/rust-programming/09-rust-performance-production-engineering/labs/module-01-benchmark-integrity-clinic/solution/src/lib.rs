use std::hint::black_box;
use std::time::{Duration, Instant};

#[derive(Debug, Clone)]
pub struct Workload {
    pub name: String,
    pub bytes: Vec<u8>,
    pub iterations: usize,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Observation {
    pub elapsed: Duration,
    pub result: u64,
    pub bytes_processed: usize,
}

pub fn checksum(bytes: &[u8]) -> u64 {
    bytes
        .iter()
        .fold(0xcbf2_9ce4_8422_2325_u64, |acc, &byte| {
            (acc ^ u64::from(byte)).wrapping_mul(0x1000_0000_01b3)
        })
}

pub fn expected_result(input: &[u8], iterations: usize) -> u64 {
    let value = checksum(input);
    if iterations.is_multiple_of(2) { 0 } else { value }
}

pub fn measure(workload: &Workload) -> Result<Observation, &'static str> {
    if workload.iterations == 0 {
        return Err("iterations must be nonzero");
    }
    let bytes_processed = workload
        .bytes
        .len()
        .checked_mul(workload.iterations)
        .ok_or("byte count overflow")?;

    let started = Instant::now();
    let mut result = 0_u64;
    for _ in 0..workload.iterations {
        result ^= checksum(black_box(&workload.bytes));
    }
    let elapsed = started.elapsed();
    let result = black_box(result);

    if result != expected_result(&workload.bytes, workload.iterations) {
        return Err("correctness oracle failed");
    }

    Ok(Observation { elapsed, result, bytes_processed })
}

pub fn parameterized_workloads() -> Vec<Workload> {
    [64_usize, 4096, 65_536]
        .into_iter()
        .map(|size| Workload {
            name: format!("bytes-{size}"),
            bytes: vec![b'x'; size],
            iterations: 1001,
        })
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn oracle_matches_loop_parity() {
        assert_eq!(expected_result(b"x", 2), 0);
        assert_eq!(expected_result(b"x", 3), checksum(b"x"));
    }

    #[test]
    fn measurement_preserves_oracle_and_accounting() {
        let workload = Workload {
            name: "small".to_owned(),
            bytes: vec![1, 2, 3],
            iterations: 5,
        };
        let observed = measure(&workload).expect("valid workload");
        assert_eq!(observed.result, checksum(&workload.bytes));
        assert_eq!(observed.bytes_processed, 15);
    }

    #[test]
    fn zero_iterations_are_rejected() {
        let workload = Workload {
            name: "invalid".to_owned(),
            bytes: vec![1],
            iterations: 0,
        };
        assert_eq!(measure(&workload), Err("iterations must be nonzero"));
    }
}
