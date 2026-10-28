#![allow(dead_code)]
use std::future::Future;
fn spawn_contract<F>(_: F) where F: Future<Output = usize> + Send + 'static {}
fn main() { let text = String::from("owned"); spawn_contract(async move { text.len() }); }
