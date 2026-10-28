#![allow(dead_code)]
use std::future::{ready, Future};
fn require_future<F: Future<Output = usize>>(_: F) {}
fn main() { require_future(async { ready(20usize).await + 2 }); }
