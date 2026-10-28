use std::time::Instant; fn main() { let started = Instant::now(); let input = vec![0_u8; 1_000_000]; let elapsed = started.elapsed(); println!("{} {}", input.len(), elapsed.as_nanos()); }
