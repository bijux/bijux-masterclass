#![allow(dead_code)]
use std::future::Future;
fn spawn_contract<F: Future + Send + 'static>(_: F) {}
fn main() { let token = String::from("owned"); spawn_contract(async move { token.len() }); println!("{token}"); }
