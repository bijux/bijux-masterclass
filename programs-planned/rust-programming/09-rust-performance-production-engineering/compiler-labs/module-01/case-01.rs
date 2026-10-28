fn measured(value: u64) -> u64 { value.wrapping_mul(2) } fn main() { assert_eq!(measured(4), 8); }
