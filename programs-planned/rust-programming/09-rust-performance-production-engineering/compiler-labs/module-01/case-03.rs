fn bytes(count: usize, width: usize) -> Option<usize> { count.checked_mul(width) } fn main() { assert_eq!(bytes(4, 8), Some(32)); }
