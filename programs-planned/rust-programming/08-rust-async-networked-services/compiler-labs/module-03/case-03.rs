#![allow(dead_code)]
fn take_buffer(buffer: &mut Vec<u8>) -> Vec<u8> { std::mem::take(buffer) }
fn main() { let mut pending = vec![1,2,3]; let frame = take_buffer(&mut pending); assert!(pending.is_empty()); assert_eq!(frame.len(),3); }
