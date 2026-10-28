use std::hint::black_box; fn checksum(v: &[u8]) -> u64 { v.iter().map(|&b| u64::from(b)).sum() } fn main() { let input = [1,2,3,4]; assert_eq!(black_box(checksum(black_box(&input))), 10); }
