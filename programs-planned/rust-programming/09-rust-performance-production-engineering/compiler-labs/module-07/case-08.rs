fn main() { let mut attempt = 0_u64; loop { attempt += 1; if attempt == 1_000_000 { break; } } println!("{attempt}"); }
