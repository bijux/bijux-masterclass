#![allow(dead_code)]
use std::future::Future;
fn run_service<F: Future + Send + 'static>(_: F) {}
fn main() { let config = String::from("borrowed"); run_service(async { config.len() }); }
