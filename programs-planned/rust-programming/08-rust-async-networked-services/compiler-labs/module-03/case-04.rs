#![allow(dead_code)]
struct Frame<'a> { payload: &'a [u8] }
fn parse(bytes: &[u8]) -> Frame<'_> { Frame { payload: bytes } }
fn main() { let data = vec![4,5]; let frame = parse(&data); assert_eq!(frame.payload, &[4,5]); }
