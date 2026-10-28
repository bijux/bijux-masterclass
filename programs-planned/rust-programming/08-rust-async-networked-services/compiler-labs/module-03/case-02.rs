#![allow(dead_code)]
fn split_frame(bytes: &[u8], length: usize) -> Option<(&[u8], &[u8])> { if bytes.len() < length { None } else { Some(bytes.split_at(length)) } }
fn main() { let (frame, rest) = split_frame(b"abcde", 3).unwrap(); assert_eq!((frame, rest), (&b"abc"[..], &b"de"[..])); }
