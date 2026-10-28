#![allow(dead_code)]
fn decode_u32(bytes: &[u8]) -> Option<u32> { let raw: [u8; 4] = bytes.get(..4)?.try_into().ok()?; Some(u32::from_be_bytes(raw)) }
fn main() { assert_eq!(decode_u32(&[0,0,0,7]), Some(7)); }
