#![allow(dead_code)]
fn consume(_: Vec<u8>) {}
fn main() { let buffer = vec![1u8,2,3]; let view = &buffer[..]; consume(buffer); println!("{}", view.len()); }
