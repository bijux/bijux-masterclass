#![allow(dead_code)]
fn attempt(key: String) -> usize { key.len() }
fn main() { let key = String::from("stable-key"); let first = attempt(key.clone()); let second = attempt(key); assert_eq!(first, second); }
