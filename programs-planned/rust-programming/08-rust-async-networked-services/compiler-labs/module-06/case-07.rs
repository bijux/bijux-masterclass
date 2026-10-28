#![allow(dead_code)]
use std::collections::VecDeque;
fn main() { let mut queue = VecDeque::from([1,2]); let first = queue.front_mut().unwrap(); let second = queue.back_mut().unwrap(); *first += *second; }
