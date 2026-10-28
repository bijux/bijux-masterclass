#![allow(dead_code)]
use std::{future::Future, sync::Arc};
fn spawn_contract<F: Future + Send + 'static>(_: F) {}
fn main() { let value = Arc::new(String::from("shared")); let worker = Arc::clone(&value); spawn_contract(async move { worker.len() }); assert_eq!(value.len(), 6); }
