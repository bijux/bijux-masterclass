fn reusable(mut v: Vec<u8>, maximum: usize) -> Option<Vec<u8>> { v.clear(); (v.capacity() <= maximum).then_some(v) } fn main() { assert!(reusable(Vec::with_capacity(8), 16).is_some()); }
