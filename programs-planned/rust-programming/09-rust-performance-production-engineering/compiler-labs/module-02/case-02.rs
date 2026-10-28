fn linear(values: &[u64]) -> u64 { values.iter().copied().sum() } fn main() { assert_eq!(linear(&[1,2,3]), 6); }
