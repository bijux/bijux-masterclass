fn total(count: usize, bytes_each: usize, fixed: usize) -> Option<usize> { count.checked_mul(bytes_each)?.checked_add(fixed) } fn main() { assert_eq!(total(10, 4, 2), Some(42)); }
