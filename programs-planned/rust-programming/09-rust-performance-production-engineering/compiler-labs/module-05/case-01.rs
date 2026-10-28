fn queue_bytes(items: usize, bytes_each: usize) -> Option<usize> { items.checked_mul(bytes_each) } fn main() { assert_eq!(queue_bytes(128, 512), Some(65_536)); }
