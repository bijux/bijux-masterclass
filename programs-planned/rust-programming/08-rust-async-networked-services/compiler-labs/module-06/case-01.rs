#![allow(dead_code)]
#[derive(Clone, Copy)] struct Capacity(usize);
impl Capacity { fn new(value: usize) -> Option<Self> { (value > 0).then_some(Self(value)) } }
fn main() { assert_eq!(Capacity::new(4).map(|c| c.0), Some(4)); }
