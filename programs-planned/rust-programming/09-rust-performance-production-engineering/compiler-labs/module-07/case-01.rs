fn budget(total_ms: u64, elapsed_ms: u64) -> Option<u64> { total_ms.checked_sub(elapsed_ms) } fn main() { assert_eq!(budget(750, 200), Some(550)); }
