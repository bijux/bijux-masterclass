fn reserved(values: &Vec<u8>) -> usize { values.capacity() } fn main() { let mut v = Vec::with_capacity(128); v.push(1); assert!(reserved(&v) >= 128); }
