#![allow(dead_code)]
use std::{future::{ready, Future}, rc::Rc};
fn run_service<F: Future + Send + 'static>(_: F) {}
fn main() { let registry = Rc::new(vec![1u8]); run_service(async move { ready(()).await; registry.len() }); }
