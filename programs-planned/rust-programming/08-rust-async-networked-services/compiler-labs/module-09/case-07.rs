#![allow(dead_code)]
use std::future::Future;
fn detached<F: Future + 'static>(_: F) {}
fn main() { let schedule = [1u64,2,3]; detached(async { schedule[0] }); }
