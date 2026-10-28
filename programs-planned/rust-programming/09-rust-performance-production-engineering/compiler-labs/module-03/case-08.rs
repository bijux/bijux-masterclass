use std::collections::HashMap; fn main() { let mut cache = HashMap::new(); for n in 0..100_000 { cache.insert(n, vec![0_u8; 1024]); } println!("{}", cache.len()); }
