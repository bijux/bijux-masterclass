#![allow(dead_code)]
use std::sync::{Arc, atomic::{AtomicBool, Ordering}};
#[derive(Clone)] struct Cancellation { flag: Arc<AtomicBool> }
impl Cancellation { fn cancel(&self) { self.flag.store(true, Ordering::Release); } fn is_cancelled(&self) -> bool { self.flag.load(Ordering::Acquire) } }
fn main() { let token = Cancellation { flag: Arc::new(AtomicBool::new(false)) }; let child = token.clone(); token.cancel(); assert!(child.is_cancelled()); }
