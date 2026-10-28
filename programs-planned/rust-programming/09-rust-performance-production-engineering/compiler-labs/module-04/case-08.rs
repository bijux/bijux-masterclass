use std::sync::Arc; fn main() { let frame = Arc::new(vec![0_u8; 1_000_000]); let field = Arc::clone(&frame); println!("{}", field[0]); }
