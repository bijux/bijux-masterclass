use std::collections::VecDeque; fn main() { let mut queue = VecDeque::new(); for item in 0..1_000_000 { queue.push_back(item); } println!("{}", queue.len()); }
