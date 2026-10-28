fn escaped() -> &'static [u8] { let local = vec![1_u8,2,3]; &local } fn main() { println!("{:?}", escaped()); }
