#![allow(dead_code)]
use std::future::Future;
fn require_static<F: Future + 'static>(_: F) {}
fn main() { let deadline = 10u64; require_static(async { deadline + 1 }); }
