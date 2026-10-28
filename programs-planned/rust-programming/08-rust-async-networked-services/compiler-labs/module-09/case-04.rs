#![allow(dead_code)]
const BACKOFF_MS: [u64; 4] = [10, 25, 50, 100];
fn main() { assert_eq!(BACKOFF_MS.iter().copied().sum::<u64>(), 185); }
