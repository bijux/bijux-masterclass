fn main() { #[inline(always)] fn tiny(v: u64) -> u64 { v + 1 } println!("{}", tiny(4)); }
