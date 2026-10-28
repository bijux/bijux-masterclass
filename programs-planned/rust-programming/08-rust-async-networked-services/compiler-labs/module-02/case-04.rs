#![allow(dead_code)]
use std::future::Future;
struct Nursery;
impl Nursery { fn spawn<F: Future + Send + 'static>(&mut self, _: F) {} }
fn main() { let mut nursery = Nursery; nursery.spawn(async move { 4usize }); }
