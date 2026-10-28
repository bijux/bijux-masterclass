#![allow(dead_code)]
fn main() { let mut buffer = vec![1u8,2,3]; let header = &buffer[..2]; buffer.push(4); println!("{}", header[0]); }
