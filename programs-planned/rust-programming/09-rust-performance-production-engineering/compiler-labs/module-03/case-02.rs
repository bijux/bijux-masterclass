use std::sync::Arc; fn main() { let data = Arc::new(vec![1_u8; 16]); let other = Arc::clone(&data); assert_eq!(Arc::strong_count(&data), 2); drop(other); }
