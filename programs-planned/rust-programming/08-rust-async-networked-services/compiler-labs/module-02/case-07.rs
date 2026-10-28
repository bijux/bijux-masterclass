#![allow(dead_code)]
use std::{future::Future, rc::Rc};
fn task_contract<F>(_: F) where F: Future + Send + 'static, F::Output: Send + 'static {}
fn main() { task_contract(async move { Rc::new(5u8) }); }
