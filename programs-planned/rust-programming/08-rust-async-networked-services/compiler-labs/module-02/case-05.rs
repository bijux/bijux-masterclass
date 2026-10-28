#![allow(dead_code)]
use std::future::Future;
fn spawn_contract<F: Future + Send + 'static>(_: F) {}
fn main() { let text = String::from("parent"); spawn_contract(async { text.len() }); }
