#![allow(dead_code)]
use std::collections::VecDeque;
struct Broker<T> { pending: VecDeque<T>, active: usize, limit: usize }
impl<T> Broker<T> { fn can_start(&self) -> bool { self.active < self.limit && !self.pending.is_empty() } }
fn main() { let broker = Broker { pending: VecDeque::from([1]), active: 0, limit: 1 }; assert!(broker.can_start()); }
