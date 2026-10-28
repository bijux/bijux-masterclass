#![allow(dead_code, unused_imports, unused_variables)]
fn read(bytes: &[u8]) -> Option<u16> { let field = bytes.get(1..3)?; Some(u16::from_le_bytes([field[0], field[1]])) } fn main() { assert_eq!(read(&[9, 2, 0]), Some(2)); }
