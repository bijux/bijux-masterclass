use std::hint::black_box; fn main() { let value = black_box(21_u64); assert_eq!(black_box(value * 2), 42); }
