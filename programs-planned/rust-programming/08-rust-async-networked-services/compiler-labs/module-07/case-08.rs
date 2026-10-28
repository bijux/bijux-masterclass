#![allow(dead_code)]
fn main() { let mut state = 0u8; let first = async { state += 1; }; let second = async { state += 1; }; drop((first, second)); }
