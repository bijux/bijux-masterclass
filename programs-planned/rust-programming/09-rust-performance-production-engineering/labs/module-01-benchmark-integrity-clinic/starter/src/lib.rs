use std::hint::black_box;
use std::time::{Duration, Instant};

pub fn checksum(bytes: &[u8]) -> u64 {
    bytes
        .iter()
        .fold(0xcbf2_9ce4_8422_2325_u64, |acc, &byte| {
            (acc ^ u64::from(byte)).wrapping_mul(0x1000_0000_01b3)
        })
}

pub fn smoke_measure(input: &[u8], iterations: usize) -> (Duration, u64) {
    let started = Instant::now();
    let mut result = 0_u64;
    for _ in 0..iterations {
        result ^= checksum(black_box(input));
    }
    (started.elapsed(), black_box(result))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn checksum_is_stable() {
        assert_eq!(checksum(b"metric"), checksum(b"metric"));
        assert_ne!(checksum(b"metric"), checksum(b"metrics"));
    }
}
