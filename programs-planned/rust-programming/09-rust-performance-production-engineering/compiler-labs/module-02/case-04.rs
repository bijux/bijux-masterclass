fn cost(n: u64, k: u64) -> Option<u64> { n.checked_add(k.checked_mul(k.ilog2().max(1) as u64)?) } fn main() { assert!(cost(100, 8).is_some()); }
